# Observations

This is (rough and incomplete) sketch of some ideas, questions, thoughts, etc. from working with the data.

## General

For the time series data, I've upsampled everything to 30-second intervals over the reporting period 2024-01-18 04:48:30 UTC → 2024-02-17 20:57:30 UTC. The general idea is the upsampling provides the highest degree of granularity for analysis.

However, it is not clear whether the expectation is that every tower-metric pair should be reporting on this basis, as this choice of interval is inferred from the data set provided.

## Metrics

### Radio Communications

- Massive gap(s) for tower D (mean: 9+ hours, max 4+ days) relative to other towers (mean: max: c. 2 hours)
    - Also, deterioration from 40 to to just about 25 over the reporting period 
- Curious what would lead to markedly higher `radio_signal_to_noise_ratio` (mean and variance) for towers C, D vs. A, B
- Wonder what happened on February 9th to cause this metric to deteriorate drastically in the same way for towers A, B

### LTE Communications

- Curious about the spike in LTE signal-to-noise for tower D on February 12th; seems to be driven by component metrics.
     - `lte_signal_received_power`, `lte_signal_received_quality` also spikes at that time.
     - Seemingly, an improvement based on my nominal understanding of these measures.

### Computer System Performance

- `message_publish_subscribe_latency_ms` not included in the provided data
- Is system uptime measured in *decaseconds* (i.e., 1 decasecond = 10 seconds)? Seems that way for the cycle times to corroborate with timestamps in peak-to-peak comparisons.
- In general, it seems like `system_uptime` is around 18 days, but there are few hiccups (of significantly) shorter cycle times (as measured by peak-to-peak comparisons).
    - Curious why there might be these anomalies -- a monotonic clock should always count up when it's reset.
    - Is the uptime calculated from a wall clock that might be subject to stepping? (That wouldn't make very much sense!)

### Tower Power

- Only tower B showing large variation in `battery_percent` (form c. 20 to 95%, 70% on average)
    - `slave*_state_of_charge_percent` missing for towers A, C, D
    - `contactor_solar_powerport_charging` all `0` for towers A, C, D
    - `solar_voltage` missing, all `0` (or near `0`) for towers A, C, D
- Makes me highly suspicious of power readings coming from tower A, C, D
    - Not entirely sure what the typical power consumption profile of a tower is, but there is not an identifiable pattern across the four towers!
- Interesting to see decently strong positive correlation (c. 0.6 R-sq) between power and camera sensor temperatures

### Satellite Backhaul Communications

- Satellite metrics have very sparse data (none from Towers C, D; virtually nothing from A and only about quarter of interval periods reporting for B).
- Could be due to varying functionality across towers?

### Radio Frequency Detection

- Dearth of data for `radio_frequency_detection_count` (tower A missing entirely, B & C mising >99%)
- Dearth of data for `radio_frequency_precise_location_detection_count` (<1% coverage, and only for towers B, C)
- Makes me question these towers are uniform (or not) in their functionality.

### Computer Vision Pipeline

- Tower D showing 2-3x `computer_vision_tracking_latency_ms` from c. February 5th until February 13th

### Camera Health

- Tower B's `camera_drifting_pixels` has some massive outliers relative to Tower A's.
- `camera_seconds_since_nuc` is a strange metric, as there are some significant outliers across all towers.
    - I *think* this is reporting the time (in seconds) between **non-uniformity correction** (NUC) of one (or more?) infrared camera(s).
- Strong correlations between:
    - Tower A: `camera_drifting_pixels` vs. `camera_fpa_temperature` (R-sq 0.63)
    - Tower B: `camera_drifting_pixels` vs. `camera_fpa_temperature` (R-sq 0.41)

### Track Creation

- Massive outliers; unsure how these are related to one another. 
