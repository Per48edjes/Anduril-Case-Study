declare metric_names array<string>;
declare i INT64 default 0;

set metric_names = (
    select array_agg(distinct metric_name)
    from `raw_data.long`
  );

while i < array_length(metric_names) do
  execute immediate
    format(
      """
      create or replace table metrics.%s as
      select
        s.timestamp_ms as timestamp_ms,
        timestamp_millis(cast(s.timestamp_ms as int64)) as ts,
        max(if(tower_id = 'tower-A', metric_value, NULL)) as tower_A,
        max(if(tower_id = 'tower-B', metric_value, NULL)) as tower_B,
        max(if(tower_id = 'tower-C', metric_value, NULL)) as tower_C,
        max(if(tower_id = 'tower-D', metric_value, NULL)) as tower_D
      from `dim.timestamp_spine` as s
      left join `raw_data.long` as l
        on s.timestamp_ms = l.timestamp_ms
        and l.metric_name = @metric_name
      group by 1
      """, metric_names[offset(i)])
  using metric_names[offset(i)] as metric_name;
  set i = i + 1;
end while;
