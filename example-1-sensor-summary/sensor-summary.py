# ----------------------------------------------------------------------
# sglux GmbH - digiprobe USB - ModBus python demonstration
# Author: Stefan Langer

import serial
import struct
from time import sleep
import minimalmodbus
from tqdm import tqdm
import serial.tools.list_ports

def verfmm(vhex):
    return str(vhex>>8)+"."+str(vhex & 0x00ff)
def verfint(vint):
    return "{:2.3}".format(vint / 100)
def formh4(vhex):
    return  "0x{:04x}".format(vhex)

# ----------------------------------------------------------------------
# Open serial port and configure it correctly for 8E1 at 115200 Baud
def get_myport():
    myport =''
    for port in serial.tools.list_ports.comports():
        if (port.vid == 0x0403 and port.pid == 0x6015): #FTDI: VID:PID=0403:6015
            myport = str(port).split(" ")[0]
    return myport

def main(komport,fname,samples):
    # ----------------------------------------------------------------------
    # Open serial port and configure it correctly for 8E1 at 115200 Baud
    digiprobe = minimalmodbus.Instrument(komport, 1, mode='rtu')
    digiprobe.serial.baudrate   = 115200
    digiprobe.serial.bytesize   = 8
    digiprobe.serial.parity     = serial.PARITY_EVEN
    digiprobe.serial.stopbits   = 1
    digiprobe.serial.timeout    = 0.2

    name = fname+'-sn'+str(digiprobe.read_long(104, signed=False))+".log"
    f = open(name,'w')
    # ----------------------------------------------------------------------
    # print sensor information
    print ('-- READ ----------------------------------------- DEVICE INFO --')
    print ('------------------------------------------------- DEVICE INFO --', file=f)
    print ("Vendor Name     :",digiprobe.read_string(110, number_of_registers=8), file=f)
    print ("Product Type    :",digiprobe.read_string(118, number_of_registers=8), file=f)
    print ("Hardware Rev.   :",verfmm(digiprobe.read_register(100, signed=False)), file=f)
    print ("Firmware Rev.   :",verfmm(digiprobe.read_register(101, signed=False)), file=f)
    print ("Serial No.      :",digiprobe.read_long(104, signed=False), file=f)
    print ("Sensor Name     :",digiprobe.read_string(126, number_of_registers=8), file=f)
    print ('', file=f)

    # ----------------------------------------------------------------------
    # print calibration information
    print ('-- READ ------------------------------------ CALIBRATION INFO --')
    print ('-------------------------------------------- CALIBRATION INFO --', file=f)
    print ("Calibration Date:",digiprobe.read_long(1030, signed=False), file=f)
    print ("Temp. Offset    :",digiprobe.read_register(1000, signed=True), file=f)
    print ("Sensor Offset   :",digiprobe.read_register(1002, signed=True), file=f)
    calname = []
    for x in range(0,5):
        # check if the calibration is valid or not
        if (digiprobe.read_float((1003+x*2)) > 1e-28):
            calname.append(digiprobe.read_string((1032+x*8), number_of_registers=8))
        else:
            calname.append('{not available}')
        print ("Calibr.",str(x+1),"Name  :",calname[x], file=f)
    print ('', file=f)

    # ----------------------------------------------------------------------
    # print measurement data, simple form, not garanteed to be the same sample
    print ('-- READ ------------------------------------- SIMPLE DATA SET --')
    print ('--------------------------------------------- SIMPLE DATA SET --', file=f)
    print ("Raw Value       :",digiprobe.read_long(1998, signed=True), file=f)
    print ("Cycle Count     :",digiprobe.read_register(2000), file=f)
    print ("Sensor Status   :",digiprobe.read_register(2001), file=f)
    print ("Time Stamp      :",digiprobe.read_long(2002, signed=False), file=f)
    print ("Irradiance 1    : {:.5E}".format(digiprobe.read_float(2004)), file=f)
    print ("Irradiance 2    : {:.5E}".format(digiprobe.read_float(2006)), file=f)
    print ("Irradiance 3    : {:.5E}".format(digiprobe.read_float(2008)), file=f)
    print ("Irradiance 4    : {:.5E}".format(digiprobe.read_float(2010)), file=f)
    print ("Irradiance 5    : {:.5E}".format(digiprobe.read_float(2012)), file=f)
    print ("Temperature     : {:.2f}".format(digiprobe.read_float(2014)), file=f)
    print ('', file=f)

    # ----------------------------------------------------------------------
    # Print measurement data (recommended method, should be used to keep
    # correllation of cycles and time intact. It also checks that a new
    # reading has taken place by checking the cycle register has increased.
    # As long as you read the same cycle register value no new data has been
    # measured and data should not be used.
    # If the cycle increases by more than 1 a number of readings has been
    # not requested, most likely because the requests came to late - thus
    # speed up the request loop a bit. Requesting data every 50ms is fast
    # enough to capture all readings the ADC can deliver.
    # It is also important to assess the status register! Only if status is zero
    # a valid measurement has been taken. all non-zero statuses show either
    # over- or underrange condition and the value must not be trusted.
    # Most prominent use is to check if the radiation intensity was too
    # high for the measurement range of the sensor.

    print ('-- READ ------------------------------ LARGER DATA SET AS CSV --')
    print ('-------------------------------------- LARGER DATA SET AS CSV --', file=f)
    print ("cycle;status;mstime;raw-value;irradiance1;irradiance2;irradiance3;irradiance4;irradiance5;temperature;missed", file=f)
    cycle = 0 # used to check if a new measurement was completed
    missed = 0 # how many samples where missing
    cycle_last = cycle
    for x in tqdm(range(0,samples), unit=' Samples', desc='   Readings '): # we want 10 consecutive measurements
        # this while loop ensures no measurement is read twice and sensor is not asked too often
        while True:
            # read a register set
            regs = digiprobe.read_registers(1998, number_of_registers=18)
            # check if the cycle register (2000) has changed since last reading
            if(cycle != regs[2]):
                # if it has changed we break from the while loop and print the data
                cycle = regs[2]  # remember current cycle count
                break
            else:
                # ADC sample distance is ~72ms thus we can wait ~50ms for the next sample
                sleep(0.03)
        # pack the read U16 registers to an byte array. Please note, that the
        # registers for U32 and float have to be swapped => regs[3],regs[2] etc.
        buf = struct.pack('HHHHHHHHHHHHHHHHHH',regs[2],regs[3],regs[5],regs[4],regs[1],regs[0],regs[7],regs[6],regs[9],regs[8],regs[11],regs[10],regs[13],regs[12],regs[15],regs[14],regs[17],regs[16])
        if ((cycle_last == 0) or (regs[2]-cycle_last)==1):
            # we got either the first reading, or cycle has increased by exactly 1
            # which is the wanted behaviour
            cyctxt = "0"
        else:
            # cycle has increased by more than 1, so a number of samples have not been read
            cyctxt = str(regs[2]-cycle_last-1)
            missed = missed + regs[2]-cycle_last-1
        # unpack it according to data types and put into a list
        tl = list(struct.unpack('HHLlffffff',buf))
        print(*tl,cyctxt,sep=';',file=f)
        cycle_last = regs[2]
    if (missed==0):
        print('\033[32m   No missing samples, perfect!\033[0m')
    else:
        print("\033[91m   This time we missed",missed,"cycles - sample loss is {:.1f} %!".format(missed/(samples+missed)*100),"\033[0m")
    # ----------------------------------------------------------------------
    # close the port
    digiprobe.serial.close()
    f.close()
    return name

# run main!
if __name__ == '__main__':
    # determine if there is a sensor and on which port
    komport = get_myport()
    if komport =='':
        print('\033[91m\r\nNo supported sensor was found. Exiting.')
    else:
        print('\r\nReading data from sensor on port',komport,'...\r\n\033[32m')
        # define name prefix of logfile
        fname = 'digiprobe'
        # read the sensor parameters and a larger sample set into a CSV file
        outf=main(komport,fname,100)
        # list the CSV content
        print('\r\nWhat data did we get:')
        print('\033[34m')
        with open(outf,'r') as fin:
            print(fin.read())
