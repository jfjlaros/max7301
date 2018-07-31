#!/usr/bin/env python
import serial
import struct
import time


class MAX7301(object):
    OUTPUT = 0x01
    INPUT = 0x02
    INPUT_PULLUP = 0x03
    LOW = 0x00
    HIGH = 0x01

    def __init__(self):
        self._connection = serial.Serial('/dev/ttyACM0')
        self._commands = [
            'enable', 'disable', 'pinmode', 'get_pinmode', 'conf_td',
            'enable_td', 'dig_read', 'dig_write', 'read', 'write', 'int']

    def cmd(self, command, *args):
        self._connection.write(struct.pack(
            'BBB', self._commands.index(command),
            *(args + (0,) * (2 - len(args)))))

    def pin_mode(self, pin, mode):
        self.cmd('pinmode', pin, mode)

    def digital_read(self, pin):
        self.cmd('dig_read', pin)
        return ord(self._connection.read(1))

    def digital_write(self, pin, data):
        self.cmd('dig_write', pin, data)

    def read(self, address):
        self.cmd('read', address)
        return ord(self._connection.read(1))

    def check_interrupt(self):
        self.cmd('int')
        return ord(self._connection.read(1))

    def pulse(self, pin, duration):
        digital_write(pin, self.HIGH)
        time.sleep(duration)
        digital_write(pin, self.LOW)

    def dump(self):
        for address in range(0x60):
            data = max7301.read(address)
            print '0x{:02x}: 0x{:02x} 0b{:08b}'.format(address, data, data)


def main():
    max7301 = MAX7301()

    max7301.cmd('enable')
    max7301.pin_mode(12, MAX7301.INPUT_PULLUP)
    max7301.pin_mode(22, MAX7301.OUTPUT)

    max7301.pin_mode(31, MAX7301.OUTPUT)
    max7301.pin_mode(24, MAX7301.INPUT_PULLUP)
    max7301.cmd('conf_td', 24, True)
    max7301.cmd('enable_td')

    max7301.digital_write(22, MAX7301.LOW)

    while True:
        if not max7301.digital_read(12):
            max7301.pulse(22, 0.2)

        if max7301.check_interrupt:
            max7301.pulse(22, 0.2)
            max7301.cmd('enable_td')

        time.sleep(1.0)


if __name__ == '__main__':
    main()
