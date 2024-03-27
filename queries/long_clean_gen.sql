create or replace table raw_data.long_clean as (
select
  timestamp_ms,
  timestamp_millis(cast(timestamp_ms as int64)) as ts,
  replace(tower_id, '-', '_') as tower_id,
  metric_name,
  metric_value
from `raw_data.long`
);