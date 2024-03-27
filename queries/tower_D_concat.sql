create or replace table raw_data.tower_D as (
  select * from `raw_data.tower_D`
  union all
  select * from `raw_data.tower_D_bonus`
);
