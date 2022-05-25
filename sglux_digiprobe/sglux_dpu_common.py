#!/usr/bin/env python3

from asyncio.windows_events import NULL
import serial.tools.list_ports
import minimalmodbus

# ----------------------------------------------------------------------
# Find serial ports that match the correct PID:VID pair
def get_myport():
    myport =''
    for port in serial.tools.list_ports.comports():
        if (port.vid == 0x0403 and port.pid == 0x6015):
            myport = str(port).split(" ")[0]
    return myport

# use simplified form for USB because all parameters are locked
def open_usb(port, timeout):
    usb = open_port(port=port, id=1, mode='rtu', baud=115200, bytesize=8, parity=serial.PARITY_EVEN, stop=1, timeout=timeout)
    return usb

# use extended form for RS485, enabling some checks later
def open_rs485(port, id, mode, baud, bytesize, parity, stop, timeout):
    rs485 = open_port(port, id, mode, baud, bytesize, parity, stop, timeout)
    return rs485

# ----------------------------------------------------------------------
# Open serial port and configure it
def open_port(port,id,mode,baud,bytesize,parity,stop,timeout):
    try:
        opened = minimalmodbus.Instrument(port, id, mode)
    except:
        pass        
    opened.serial.baudrate   = baud
    opened.serial.bytesize   = bytesize
    opened.serial.parity     = parity
    opened.serial.stopbits   = stop
    opened.serial.timeout    = timeout
    return opened

def lsprint(text,outfile):
    print(text)
    print(text,file=outfile)

# format 16Bit version number to hex string with comma
def verfmm(vhex):
    return str(vhex>>8)+"."+str(vhex & 0x00ff)

# format 16Bit version number to decimal string
def verfint(vint):
    return "{:2.3}".format(vint / 100)

# format 16Bit version number to hex string without comma
def formh4(vhex):
    return "0x{:04x}".format(vhex)

if __name__ == '__main__':
    print('This script is intended to be imported in other python programs.\n\rIt does nothing by intention if started directly.')