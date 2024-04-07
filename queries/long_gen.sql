create or replace table raw_data.long as (
  select * from `raw_data.tower_A`
  union distinct
  select * from `raw_data.tower_B`
  union distinct
  select * from `raw_data.tower_C`
  union distinct
  select * from `raw_data.tower_D`
);
