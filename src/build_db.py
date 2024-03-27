#!/usr/bin/env python

import json
import os

import pandas as pd
import pandas_gbq
from dotenv import load_dotenv
from google.cloud import bigquery as bq

from config import ARTIFACTS_DIR, QUERIES_DIR, setup_logging


def build_bonus_table():
    project_id = os.getenv("PROJECT_ID")

    with open(os.path.join(ARTIFACTS_DIR, "bonus.json"), "r", encoding="utf-8") as f:
        contents = f.readlines()
        blobs = list(map(json.loads, contents))

    rows = []
    for blob in filter(lambda b: b["series"], blobs):
        [data] = blob["series"]
        metric, host, points = data["metric"], data["scope"], data["pointlist"]
        host = host.split(":")[-1]
        points = [
            {
                "tower_id": host,
                "timestamp_ms": timestamp_ms,
                "metric_name": metric,
                "metric_value": metric_value,
            }
            for timestamp_ms, metric_value in points
        ]
        rows.extend(points)

    df = pd.DataFrame(rows)
    pandas_gbq.to_gbq(
        df, "raw_data.tower_D_bonus", project_id=project_id, if_exists="replace"
    )


if __name__ == "__main__":
    load_dotenv()

    logger = setup_logging(f"{os.path.basename(__file__).split('.')[0]}")

    # NOTE: Build bonus table from JSON data first
    build_bonus_table()

    client = bq.Client()

    # NOTE: Add queries here to execute table transformation of raw data
    # WARN: BigQuery datasets must be created before running these queries;
    #       the queries will fail if the datasets (`dim`, `raw_data`, `metrics`, `towers`) do not exist!
    GEN_QUERIES = [
        "long_gen.sql",
        "long_clean_gen.sql",
        "timestamp_spine_gen.sql",
        "tower_D_concat.sql",
        "metrics_schema_gen.sql",
        "tower_schema_gen.sql",
    ]

    queries = [os.path.join(QUERIES_DIR, q) for q in GEN_QUERIES]
    for query_src in queries:
        with open(query_src, "r") as f:
            query = f.read()

        try:
            job = client.query(query)
            logger.info(f"Job {job.job_id} started.")
            job.result()
            logger.info(f"Script created {job.num_child_jobs} child jobs.")
        except Exception as e:
            logger.error(f"Failed to execute query: {e}.")
