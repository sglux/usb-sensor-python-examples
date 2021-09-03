# USB Sensor communication

The current USB based sensors from sglux present a virtual serial port to the USB host.
They employ the royalty free Modbus protocol to transmit measurement data and receive configuration data.

The examples are valid for all [UV sensor probes from sglux](https://sglux.de/en/product-category/uv-sensors/) with the option "USB output".

Examples are: UV surface, UV cosine and UV air probes.
<p>
<img src="https://sglux.de/data-matrix/uploads/2015/11/sglux_uv-surface_UVI.jpg" height=120 alt="UV surface" style="padding:5px">&nbsp;&nbsp;
<img src="https://sglux.de/data-matrix/uploads/2015/06/sglux-uv-cosine-300x300.jpg" height=120 alt="UV cosine" style="padding:5px">&nbsp;&nbsp;
<img src="https://sglux.de/data-matrix/uploads/2015/06/sglux-uv-air-300x300.jpg" height=120 alt="UV air" style="padding:5px">
</p>

## Example 1:
This example reads a couple of sensor informations and a number of readings. All that is written do a CSV file on your desktop and displayed in the terminal as well.

Please visit the subfolder [/example-1-sensor-summary](/example-1-sensor-summary) for code and demo outoput.

## Issues
If you discover an issue or somthing does not work as expected please first start a [discussion](https://github.com/sglux/usb-sensor-python-examples/discussions) before opening an issue ticket (as these are reserved for bugs not support ;-)

Thank you!
