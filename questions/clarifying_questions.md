# Clarification Questions

*I've set up a static site with the profiled data [here](https://storage.googleapis.com/anduril-case-study/index.html) if it's helpful to see what's underpinning my first pass through the data.*

- Do you have any context about these towers? (e.g., different makes/models, are their confounding factors such as location, stage of development, etc. that might be relevant to their performance in this window?)

- Is the pattern of nullity (missing data) a consequence of this being a take-home assignment or actual reporting from real towers in the reporting period?
    - e.g., only Tower D has "bonus" metrics 
    - e.g., towers B, C, D have missing data for about three-quarters of the 30 second measurement intervals in the same places
    - e.g., towers C, D not reporting any satellite info
    - e.g., no radar detection values for towers A, B, C, 
    - etc.

- What are the specific units associated for each metric?  (I can mostly infer based on suffixes and the data, but just want to confirm). 
    - e.g., consecutive 30 second interval readings from tower A suggest `system_uptime` is measured in *decaseconds* (i.e., 1 decasecond = 10 seconds), but this seems like an odd choice even if it lines up cycle times with the timestamps

- In general, what is the expectation for my ability to *interpret* this data (having very little understanding of what some of these metrics are meant to measure, what typical values are, etc.)?
    - I have done modicum research into interpreting a few metrics, but I don't have enough time or confidence to make stronger statements without understanding the domain a little more.

- What does `camera_seconds_since_nuc` mean? 
    - Each tower has large gaps of time (order of magnitude: days) for this metric (read: large outliers).

- I suspect `pan_tilt_unit_*` metrics describe controlling the pan/tilt of a camera in the tower, but what are `radar_detections_count`, `track_count` and are all of the bonus metrics related?
    - Radar, as far as I know, is radio wave based detection vs. visual?
    - How does `radar_detections` compare to "Radio Frequency Detection" metrics?
