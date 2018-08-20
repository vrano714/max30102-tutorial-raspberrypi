# max30102-tutorial-raspberrypi
This repository is unofficial porting of Arduino sample code of MAXRESDEF117#(max30102) HR/SpO2 sensor.

MAXREFDES117#: https://www.maximintegrated.com/jp/design/reference-design-center/system-board/6300.html  
Original Arduino codes: https://github.com/MaximIntegratedRefDesTeam/RD117_ARDUINO/

Related Qiita post (Japanese): https://qiita.com/vrn/items/1ac58c61194b23af1d8c

## Files

- `max30102.py` contains a class which has some setup functions and sensor-reading functions
- `hrdump.py` uses `max30102.py` and records the values read by the sensor (sample logs are`ir.log` and `red.log`)
- `hrcalc.py` provides a function which calcs HR and SpO2 (but experimental)
- `makegraph.py` can visualize the log data (but it does not work on raspberry pi cli)

## Run

Before running, enable i2c interface, install smbus and rpi.gpio, and connect the sensor.

Note that the following pin connection is assumed in the files:

| RPi                     | HR Sensor |
| ----------------------- | --------- |
| 3.3V (pin1)             | VIN       |
| I2C_SDA1 (pin3; GPIO 2) | SDA       |
| I2C_SCL1 (pin5; GPIO 3) | SCL       |
| - (pin7; GPIO 4)        | INT       |
| GND (pin9)              | GND       |

### Record Raw Values

You can initialize the sensor by running the followings.

```python
>>> import max30102
>>> m = max30102.MAX30102()
>>> red, ir = m.read_sequential()
```

After that, `red` and `ir` should have 100 values each.

### Calculate HR / SpO2

`hrcalc.py` has a function `calc_hr_and_spo2(ir_data, red_data) -> (hr, hr_valid, spo2, spo2_valid)`
which works as an approximation of `maxim_heart_rate_and_oxygen_saturation` in the original Arduino implementaion.

**The resulting HR & SpO2 may be different between original implementation and this implementation.**

```python
# after you load red and ir
>>> import hrcalc
>>> hrcalc.calc_hr_and_spo2(ir[:100], red[:100])
 (136, True, 96.411114, True) # this shows hr is 136 and is valid, spo2 is 96% and is valid
```