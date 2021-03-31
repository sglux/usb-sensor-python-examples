# ## Example 1:

This example reads a couple of sensor informations and a number of readings. All that is written do a CSV file on your desktop and displayed in the terminal as well.

```
Reading data from sensor on port COM6 ...

-- READ ----------------------------------------- DEVICE INFO --
-- READ ------------------------------------ CALIBRATION INFO --
-- READ ------------------------------------- SIMPLE DATA SET --
-- READ ------------------------------ LARGER DATA SET AS CSV --
   Readings : 100%|██████████████████████████████| 100/100 [00:07<00:00, 13.39 Samples/s]
   No missing samples, perfect!

What data did we get:

------------------------------------------------- DEVICE INFO --
Vendor Name     : SGLUX GMBH
Product Type    : DIGIPROBE USB
Hardware Rev.   : 1.1
Firmware Rev.   : 3.0
Serial No.      : 4711
Sensor Name     : TEST-PD

-------------------------------------------- CALIBRATION INFO --
Calibration Date: 20200923
Temp. Offset    : 0
Sensor Offset   : 28
Calibr. 1 Name  : TEST-PD
Calibr. 2 Name  : {not available}
Calibr. 3 Name  : {not available}
Calibr. 4 Name  : {not available}
Calibr. 5 Name  : {not available}

--------------------------------------------- SIMPLE DATA SET --
Raw Value       : 162
Cycle Count     : 988
Sensor Status   : 0
Time Stamp      : 74648
Irradiance 1    : 1.95000E+02
Irradiance 2    : -1.00000E+00
Irradiance 3    : -1.00000E+00
Irradiance 4    : -1.00000E+00
Irradiance 5    : -1.00000E+00
Temperature     : 24.50

-------------------------------------- LARGER DATA SET AS CSV --
cycle;status;mstime;raw-value;irradiance1;irradiance2;irradiance3;irradiance4;irradiance5;temperature;missed
990;0;74723;154;182.0;-1.0;-1.0;-1.0;-1.0;24.5;0
991;1;74804;-115;-87.0;-1.0;-1.0;-1.0;-1.0;24.5;0
992;0;74880;198;226.0;-1.0;-1.0;-1.0;-1.0;24.5;0
993;0;74957;152;180.0;-1.0;-1.0;-1.0;-1.0;24.5;0
994;0;75036;170;198.0;-1.0;-1.0;-1.0;-1.0;24.5;0
995;0;75116;145;173.0;-1.0;-1.0;-1.0;-1.0;24.5;0
996;0;75192;134;162.0;-1.0;-1.0;-1.0;-1.0;24.5;0
997;0;75273;145;173.0;-1.0;-1.0;-1.0;-1.0;24.5;0
...
1087;1;82094;-10006;-9978.0;-1.0;-1.0;-1.0;-1.0;24.5;0
1088;1;82168;-10151;-10123.0;-1.0;-1.0;-1.0;-1.0;24.5;0
1089;1;82244;-3103;-3075.0;-1.0;-1.0;-1.0;-1.0;24.5;0


D:\REPOS\sglux-github\usb-sensor-python-examples>
```

> 
