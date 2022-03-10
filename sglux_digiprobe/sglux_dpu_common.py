#!/usr/bin/env python3

import serial

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

# ----------------------------------------------------------------------
# Open serial port and configure it correctly for 8E1 at 115200 Baud
def get_myport():
    myport =''
    for port in serial.tools.list_ports.comports():
        if (port.vid == 0x0403 and port.pid == 0x6015): #FTDI: VID:PID=0403:6015
            myport = str(port).split(" ")[0]
    return myport

if __name__ == '__main__':
    print('nothing here. This is to be used as import')