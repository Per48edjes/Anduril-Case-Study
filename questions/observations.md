
# Observations

This is (rough and incomplete) sketch of some ideas, questions, thoughts, etc. from working with the data.

## Metrics

### Tower Power

- Only tower B showing large variation in `battery_percent` (form c. 20 to 95%, 70% on average)
    - `slave*_state_of_charge_percent` missing for towers A, C, D
    - `contactor_solar_powerport_charging` all `0` for towers A, C, D
    - `solar_voltage` missing, all `0` (or near `0`) for towers A, C, D
- Makes me highly suspicious of power readings coming from tower A, C, D
    - Not entirely sure what the typical power consumption profile of a tower is, but there is not an identifiable pattern across the four towers!
- Interesting to see decently strong positive correlation (c. 0.6 R-sq) between power and camera sensor temperatures

# Satellite

- Satellite metrics have very sparse data (none from Towers C, D; virtually nothing from A and only about quarter of interval periods reporting for B).

### Radio

- Dearth of data for `radio_frequency_precise_location_detection_count` (<1% coverage, and only for towers B, C)


## Towers 

### Tower A


### Tower D


- Something wonky is happening near end of reporting period with Tower D.
  - Look at the crazy pan tilt speed values (breaking pipeline)
  - System uptime not as regular as Tower A or B.
  - LTE signal-to-noise ratio spikes like crazy near end of period.