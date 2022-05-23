# USB Sensor communication

The current USB based sensors from sglux present a virtual serial port to the USB host.
They employ the royalty free Modbus protocol to transmit measurement data and receive configuration data.

The examples are valid for all [UV sensor probes from sglux](https://sglux.de/en/product-category/uv-sensors/) with the option "USB output".

Examples of such sensors are: UV surface, UV cosine and UV air probes.
<p>
<img src="https://sglux.de/data-matrix/uploads/2015/11/sglux_uv-surface_UVI.jpg" height=120 alt="UV surface" style="padding:5px">&nbsp;&nbsp;
<img src="https://sglux.de/data-matrix/uploads/2015/06/sglux-uv-cosine-300x300.jpg" height=120 alt="UV cosine" style="padding:5px">&nbsp;&nbsp;
<img src="https://sglux.de/data-matrix/uploads/2015/06/sglux-uv-air-300x300.jpg" height=120 alt="UV air" style="padding:5px">
</p>

## How to run
Please download the latest code from [ZIP](https://github.com/sglux/usb-sensor-python-examples/archive/refs/heads/main.zip) oder clone the repository.
Extract to a folder of your choice. Then change you shell to that folder, no matter if you are on Windows (CMD or powershell) or Linux.
Start the individual examples by typing **python example-1-sensor-summary.py** and so on.


## Example 1:
This example reads a couple of sensor informations and a number of readings.
All that is written do a CSV file on your desktop and displayed in the terminal as well.
[Click here](https://github.com/sglux/usb-sensor-python-examples/blob/main/example-1-sensor-summary.md) for further details.

## Issues
If you discover an issue or somthing does not work as expected please first start a [discussion](https://github.com/sglux/usb-sensor-python-examples/discussions) before opening an issue ticket (as these are reserved for bugs not support ;-)

Thank you!
