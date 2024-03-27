#!/usr/bin/env python

import os

import pandas_gbq
from dotenv import load_dotenv
from ydata_profiling import ProfileReport

from config import PROFILES_DIR, QUERIES_DIR, setup_logging
from gcp_utils import upload_directory_with_transfer_manager

if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    bucket_name = os.getenv("BUCKET_NAME")

    logger = setup_logging(f"{os.path.basename(__file__).split('.')[0]}")

    # # NOTE: Add schema queries here to generate profile reports for all tables in the schema
    SCHEMAS = ["towers_table_names.sql", "metrics_table_names.sql"]

    queries = [os.path.join(QUERIES_DIR, q) for q in SCHEMAS]
    for query_src in queries:
        with open(query_src, "r") as f:
            query = f.read()

        meta_df = pandas_gbq.read_gbq(
            query,
            project_id=project_id,
            use_bqstorage_api=True,
        )

        for index, row in meta_df.iterrows():
            table_name, table_schema = row["table_name"], row["table_schema"]

            logger.info(f"Profiling {table_schema}:{table_name}.")

            df = pandas_gbq.read_gbq(
                f"select * from {table_schema}.{table_name}",
                project_id=project_id,
                use_bqstorage_api=True,
            )
            df.drop("timestamp_ms", axis=1, inplace=True)

            logger.info(f"Successfully read {table_name}.")

            try:
                profile = ProfileReport(
                    df, tsmode=True, title=f"{table_schema}:{table_name}", sortby="ts"
                )
                if not os.path.exists(
                    report_dir := os.path.join(PROFILES_DIR, str(table_schema))
                ):
                    os.makedirs(report_dir)
                profile.to_file(os.path.join(report_dir, f"{table_name}.html"))
                logger.info(f"Profile report for {table_name} saved.")

            except Exception as e:
                logger.error(f"Failed to profile {table_name}: {e}")

    # NOTE: Batch upload all profile reports to GCS
    upload_directory_with_transfer_manager(bucket_name, PROFILES_DIR)
