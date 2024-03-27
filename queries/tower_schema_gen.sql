declare tower_ids array<string>;
declare i INT64 default 0;

set tower_ids = (
    select array_agg(distinct replace(tower_id, '-', '_'))
    from `raw_data.long`
  );

while i < array_length(tower_ids) do
  execute immediate
    format(
      """
      create or replace table towers.%s as
      with 

        cte_comprehensive_ts as (
          select
            tss.timestamp_ms,
            timestamp_millis(cast(tss.timestamp_ms as int64)) as ts,
            tower.metric_name,
            tower.metric_value
          from `dim.timestamp_spine` as tss
          left join `raw_data.%s` as tower
            on tss.timestamp_ms = tower.timestamp_ms
        )


      select * 
      from cte_comprehensive_ts
        pivot(
          max(metric_value) for metric_name in (
            -- NOTE: Hardcoded because pivot column must be a constant known at compile time
            'solar_voltage', 
            'system_uptime', 
            'battery_percentage', 
            'camera_temp_sensor0', 
            'camera_temp_sensor1', 
            'camera_cooler_current', 
            'camera_drifting_pixels', 
            'camera_fpa_temperature', 
            'process_cpu_utilization', 
            'camera_seconds_since_nuc', 
            'lte_signal_received_power', 
            'lte_signal_to_noise_ratio', 
            'satellite_backhaul_uptime', 
            'lte_signal_received_quality', 
            'radio_signal_to_noise_ratio', 
            'camera_enclosure_temperature', 
            'satellite_backhaul_latency_ms', 
            'master_state_of_charge_percent', 
            'detection_rate_frames_per_second', 
            'contactor_solar_powerport_charging', 
            'computer_vision_tracking_latency_ms', 
            'all_batteries_state_of_charge_percent', 
            'satellite_backhaul_uplink_throughput_bps', 
            'satellite_backhaul_downlink_throughput_bps', 
            'slave0_state_of_charge_percent', 
            'slave1_state_of_charge_percent', 
            'slave2_state_of_charge_percent', 
            'radio_frequency_detection_count', 
            'radio_frequency_precise_location_detection_count', 
            'radio_frequency_detection_latency',
            'track_count',
            'radar_detections_count',
            'pan_tilt_unit_pan_speed',
            'pan_tilt_unit_tilt_speed',
            'pan_tilt_unit_command_elapsed_time'
          )
        );
      """, tower_ids[offset(i)], tower_ids[offset(i)]);
  set i = i + 1;
end while;
