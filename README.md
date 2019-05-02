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
If you use `hrcalc.py` to get HR and SpO2, numpy is required.

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
>>> m = max30102.MAX30102() # sensor initialization
>>> red, ir = m.read_sequential() # get LEDs readings
```

After that, `red` and `ir` should have 100 values each.

If you use different pin other than pin 7 for INT, `max30102.MAX30102()` should be modified (`gpio_pin=7` is the default value).  
If your HR sensor's address is not `0x57`, `max30102.MAX30102()` should be modified (`address=0x57` is the default value).

### Calculate HR / SpO2

`hrcalc.py` has a function `calc_hr_and_spo2(ir_data, red_data) -> (hr, hr_valid, spo2, spo2_valid)`
which works as an approximation of `maxim_heart_rate_and_oxygen_saturation` in the original Arduino implementation.

**The resulting HR & SpO2 may be different between original implementation and this implementation.**  

```python
# after you load red and ir
>>> import hrcalc
>>> hrcalc.calc_hr_and_spo2(ir[:100], red[:100]) # give 100 values
(136, True, 98.752554, True)
# this shows hr is 136 and it is a valid value, spo2 is 98% and it is a valid value
# this value is produced when using line 10 - 110 of sample logs
```

### Using sample files (ir.log, red.log)

These two files are pre-recorded sensor data. Both has 1000 lines (= 1000 values).

Tesing can be:

```python
>>> import hrcalc
>>> ir = []
>>> with open("ir.log", "r") as f:
...     for line in f:
...         ir.append(int(line))
...
>>> red = []
>>> with open("red.log", "r") as f:
...     for line in f:
...         red.append(int(line))
...
>>> for i in range(37):
...     print(hrcalc.calc_hr_and_spo2(ir[25*i:25*i+100], red[25*i:25*i+100]))
...
(-999, False, -999, False)
(107, True, 99.43662599999999, True)
(88, True, 99.519096, True)
(83, True, 99.855786, True)
(83, True, 99.59255399999999, True)
(125, True, 99.758856, True)
(100, True, 99.43662599999999, True)
(107, True, 99.657, True)
(115, True, 99.848136, True)
(136, True, 99.824664, True)
(125, True, 99.0534, True)
(100, True, 99.8058, True)
(115, True, 99.135144, True)
(93, True, 99.016626, True)
(100, True, 99.771114, True)
(88, True, 99.169194, True)
(100, True, 99.169194, True)
(107, True, 99.373746, True)
(100, True, 99.84405, True)
(125, True, 99.758856, True)
(115, True, 99.758856, True)
(88, True, 99.43662599999999, True)
(68, True, 99.345144, True)
(65, True, 99.373746, True)
(65, True, 99.373746, True)
(78, True, 99.854424, True)
(88, True, 99.712434, True)
(83, True, 99.657, True)
(93, True, 99.345144, True)
(88, True, 99.712434, True)
(88, True, 99.855786, True)
(68, True, 99.848136, True)
(68, True, 99.848136, True)
(42, True, 99.854424, True)
(71, True, 96.23505, True)
(75, True, 98.928594, True)
(83, True, 99.43662599999999, True)
```

-----

Caution: Do not use these files at critical/fatal situations. No guarantee of calculation result.
