# ----------------------------------------------------------------------
# sglux GmbH digiprobe USB / ModBus python demonstration, 2016-11-21
# Author: Stefan Langer   Environment: Windows 7, Python 3.5.1
# Modified: 2020-10-21: Devlin Thyne, Surfacide Manufacturing
# Changed read_string calls to work with MinimalModbus version 1.0

#import libraries
import serial
import array
import struct
import minimalmodbus
import time

# ----------------------------------------------------------------------
# Open serial port and configure it correctly for 8E1 at 115200 Baud
# [NOTE: on Linux/Unix you may need to change 'COM4' to '/dev/tty*'    ]
digiprobe = minimalmodbus.Instrument('COM4', 1, mode='rtu')
#digiprobe = minimalmodbus.Instrument('/dev/ttyUSB0', 1, mode='rtu')
digiprobe.serial.baudrate   = 115200
digiprobe.serial.bytesize   = 8
digiprobe.serial.parity     = serial.PARITY_EVEN
digiprobe.serial.stopbits   = 1
digiprobe.serial.timeout    = 0.2

# ----------------------------------------------------------------------
# print sensor information
print ()
print ('----------------------------------------------------------------')
print ("Product Vendor    :",digiprobe.read_string(110, number_of_registers=8))
print ("Product Type      :",digiprobe.read_string(118, number_of_registers=8))
print ("Serial Number     :",digiprobe.read_long(104, signed=False))
print ("Sensor Name       :",digiprobe.read_string(126, number_of_registers=8))
print ("Sensor Address    :",digiprobe.read_register(106))
print ("Protocol Setup    : 0x{:04x}".format(digiprobe.read_register(107)))
print ("Hardware Revision : 0x{:04x}".format(digiprobe.read_register(100)))
print ("Firmware Revision : 0x{:04x}".format(digiprobe.read_register(101)))
print ()

# ----------------------------------------------------------------------
# print calibration information
print ('----------------------------------------------------------------')
print ("Calibration Date :",digiprobe.read_long(1030, signed=False))
print ("Calibr. 1 Name   :",digiprobe.read_string(1032, number_of_registers=8))
print ("Calibr. 2 Name   :",digiprobe.read_string(1040, number_of_registers=8))
print ("Calibr. 3 Name   :",digiprobe.read_string(1048, number_of_registers=8))
print ("Calibr. 4 Name   :",digiprobe.read_string(1056, number_of_registers=8))
print ("Calibr. 5 Name   :",digiprobe.read_string(1064, number_of_registers=8))
print ()

# ----------------------------------------------------------------------
# print measurement data (simple method, should only be used if strict
# (time-)correllation of the data from different registers is not required)
print ('----------------------------------------------------------------')
print ('Single sample, all values including RAW')
print ("RAW ADC reading  :",digiprobe.read_long(1998, signed=True))
print ("Cycle Count      :",digiprobe.read_register(2000))
print ("Sensor Status    :",digiprobe.read_register(2001))
print ("Time Stamp       :",digiprobe.read_long(2002, signed=False))
print ("Irradiance 1     :",digiprobe.read_float(2004))
print ("Irradiance 2     :",digiprobe.read_float(2006))
print ("Irradiance 3     :",digiprobe.read_float(2008))
print ("Irradiance 4     :",digiprobe.read_float(2010))
print ("Irradiance 5     :",digiprobe.read_float(2012))
print ("Temperature      : {:.2f}".format(digiprobe.read_float(2014)))
print ()

# ----------------------------------------------------------------------
# Print measurement data (recommended method, should be used to keep
# correllation of cycles and time intact. It also checks that a new
# reading has taken place by checking the cycle register has changed.
# as long as you read the same cycle register value no new data has been
# measured and data should not be used.
# it is important to assess the status register! Only if status is zero
# a valid measurement has been taken. all non-zero statuses show either
# over- or underrange condition and the value must not be trusted.
# Most prominent use is to check if the radiation intensity was too
# high for the measurement range of the sensor.

print ('----------------------------------------------------------------')
print ("Printing 10 consecutive readings:")
print ("(cycle, status, mstime, rad(0), temp)")

cycle = 0 # used to check if a new measurement was completed

for x in range(0,9): # we want 10 consecutive measurements
    while True:
        #read a register set without the RAW value
        regs = digiprobe.read_registers(2000, number_of_registers=16)
        #check if the cycle register (2000) has changed since last reading
        if(cycle != regs[0]):
            #if it has changed we break from the while loop and print the data
            cycle = regs[0]  #remember current cycle count
            break
        else:
            time.sleep(0.05)
    #pack the read U16 registers to an byte array. Please note, that the
    #register types for U32 and float have to be swapped => regs[3],regs[2] etc.
    buf = struct.pack('HHHHHHHH',regs[0],regs[1],regs[3],regs[2],regs[5],regs[4],regs[15],regs[14])
    #unpack it according to data types.
    print(struct.unpack('HHLff',buf))
    
# ----------------------------------------------------------------------
# close the port
digiprobe.serial.close()

