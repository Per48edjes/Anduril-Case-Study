# Clarification Questions

*I've set up a static site with the profiled data [here](https://storage.googleapis.com/anduril-case-study/index.html) if it's helpful to see what's underpinning my first pass through the data.*

## Overview

I'm working through the open exploration of the data right now, and as I mentioned in my email, many of my questions have to do with what these numbers *mean* and investigating context about the data.

Also, I'm trying to gauge expectations re: interpretation since I don't have a hardware background that would give me more intimate underestanding of the semantics of these metrics.
Any insight around this (especially vis-a-vis the panel presentation) would be most helpful!

## Questions

- Do you have any context to share about these towers? 
    - e.g., different makes/models, 
    - e.g., confounding factors such as location, stage of development, operating conditions, etc.
    - e.g., anything notable about this period in particular,
    - etc.

- Do we expect reporting cadence for tower-metric pairs to be similar or do some towers report some metrics at varying frequencies?

- Are patterns of [nullity](https://lookerstudio.google.com/s/i0CJkONr1kE) (missing data) simply a consequence of this being a take-home assignment or actual reporting from real towers over the reporting period?
    - e.g., only Tower D has "bonus" metrics,
    - e.g., towers B, C, D have missing data for about three-quarters of the 30 second measurement intervals in the same places,
    - e.g., towers C, D not reporting any satellite info,
    - e.g., no radar detection values for towers A, B, C, 
    - etc.

- What are the specific units associated for each metric?
    - I can mostly infer based on suffixes and the data, but just want to confirm.
    - e.g., consecutive 30 second interval readings from tower A suggest `system_uptime` is measured in *decaseconds* (i.e., 1 decasecond = 10 seconds), but this seems like an odd choice even if it lines up cycle times with the timestamps
    - e.g., signal-to-noise usually reported in decibels (dB)
    - e.g., temperatures are all in reasonable ranges for Celsius and Fahrenheit scales (either in really hot or cold conditions, respectively!)

- `message_publish_subscribte_latency_ms` is a listed metric in the doc, but absent from the raw data provided. Was that intentional?

```bash
$ grep 'message_' ./tower-{A,B,C,D}.csv -c                                                                                                                                                     main      1 ↵ 
tower-A.csv:0
tower-B.csv:0
tower-C.csv:0
tower-D.csv:0
```

- What does `camera_seconds_since_nuc` mean? 
    - Each tower has large gaps of time (order of magnitude: days) for this metric (read: large outliers).

- I suspect `pan_tilt_unit_*` metrics describe controlling the pan/tilt of some camera(s?) in the tower, but what are `radar_detections_count`, `track_count` and are the bonus metrics themselves conceptually related?
    - How does `radar_detections` compare to the radio frequency detection metrics, conceptually (what are they measuring)?
    - What are the radio frequencies being detected (and to what end)?
    - How is time measured for the "speed" metrics?
