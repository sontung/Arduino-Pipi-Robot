"""
This is the code for communicating with the Pipi through bluetooth. It uses PySerial
as a main way to setup a serial connection between this app and the Pipi (or the bluetooth
module). To connect successfully, one must find his/her correct port for outgoing bluetooth.
"""
import serial


class Communication:
    def __init__(self, serial_port):
        self.serial_port = serial_port  # Bluetooth serial port
        self.connection = serial.Serial(self.serial_port)

    def write(self, val):
        """
        Send val to bluetooth module.
        :param val:
        :return:
        """
        self.connection.write(val)