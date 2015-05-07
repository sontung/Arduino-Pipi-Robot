import serial
import time
bluetooth_port = serial.Serial(11)

while True:
    time.sleep(1)
    bluetooth_port.write('0')
    time.sleep(1)
    bluetooth_port.write('1')
