create or replace table dim.timestamp_spine as (
  with

    cte_timestamps_meta as (
      select 
        min(timestamp_ms) as earliest,
        max(timestamp_ms) as latest,
        -- NOTE: This is the finest granularity of time series
        30000 as period_granularity_ms,
      from `raw_data.long`
    )


  select
    timestamp_ms
  from cte_timestamps_meta as tsm
  cross join unnest(generate_array(tsm.earliest, tsm.latest, tsm.period_granularity_ms)) as timestamp_ms
  order by 1
);
