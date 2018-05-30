# max30102-tutorial-raspberrypi
This repository is unofficial porting of Arduino sample code of MAXRESDEF117#(max30102) HR/SpO2 sensor.

MAXREFDES117#: https://www.maximintegrated.com/jp/design/reference-design-center/system-board/6300.html  
Original Arduino codes: https://github.com/MaximIntegratedRefDesTeam/RD117_ARDUINO/

Related Qiita post (Japanese): 

# Files
- `max30102.py` contains a class which has some setup functions and sensor-reading functions
- `hrdump.py` uses `max30102.py` and records the values read by the sensor (sample logs are`ir.log` and `red.log`)
- `makegraph.py` can visualize the log data (but it does not work on raspberry pi cli)

# Run
Before running enable i2c and connect the sensor.

You can initialize the sensor by running the followings.

```python
>>> import max30102
>>> m = max30102.MAX30102()
>>> red, ir = m.read_sequential()
```

After that, `red` and `ir` should have 100 values each.

**This repository does not cover HR and SpO2 calculation**
