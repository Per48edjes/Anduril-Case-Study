create or replace table raw_data.long as (
  select * from `raw_data.tower_A`
  union all
  select * from `raw_data.tower_B`
  union all
  select * from `raw_data.tower_C`
  union all
  select * from `raw_data.tower_D`
  union all
  select * from `raw_data.tower_D_bonus`
);
