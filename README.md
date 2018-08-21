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
If you use `hrcalc.py`, numpy is required.

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
which works as an approximation of `maxim_heart_rate_and_oxygen_saturation` in the original Arduino implementation.

**The resulting HR & SpO2 may be different between original implementation and this implementation.**  

```python
# after you load red and ir
>>> import hrcalc
>>> hrcalc.calc_hr_and_spo2(ir[:100], red[:100])
(136, True, 96.411114, True)
# this shows hr is 136 and it is a valid value, spo2 is 96% and it is a valid value
# this value is produced when using line 10 - 110 of sample logs
```

### Using sample files (ir.log, red.log)

these two files are pre-recorded sensor data. Both has 1000 lines (= 1000 values).

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
...     hrcalc.calc_hr_and_spo2(ir[25*i:25*i+100], red[25*i:25*i+100])
...
(-999, False, -999, False)
(166, True, 96.157416, True)
(166, True, 53.29605, True)
(136, True, 91.65938399999999, True)
(62, True, 81.02229599999998, True)
(78, True, 80.435154, True)
(78, True, 92.03925, True)
(62, True, 90.872616, True)
(62, True, 62.00625, True)
(78, True, 60.336306, True)
(115, True, 71.982216, True)
(75, True, 82.169544, True)
(88, True, 92.03925, True)
(65, True, 88.747986, True)
(65, True, 88.747986, True)
(78, True, 82.72964999999999, True)
(107, True, 92.771946, True)
(115, True, 99.519096, True)
(136, True, 49.55963399999999, True)
(100, True, 99.8058, True)
(65, True, 99.59255399999999, True)
(41, True, 98.288856, True)
(83, True, 79.233834, True)
(83, True, 79.233834, True)
(125, True, 59.48781599999999, True)
(78, True, 81.02229599999998, True)
(115, True, 68.32554599999999, True)
(83, True, 94.129194, True)
(136, True, 99.758856, True)
(125, True, 95.894706, True)
(107, True, 88.29602399999999, True)
(88, True, 88.29602399999999, True)
(100, True, 90.0498, True)
(93, True, 69.074904, True)
(107, True, 61.17578399999999, True)
(75, True, 63.640146, True)
(78, True, 97.74405, True)
```

-----

Caution: Do not use these files at critical/fatal situations. No guarantee of calculation result.