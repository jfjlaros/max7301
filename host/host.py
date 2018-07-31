#!/usr/bin/env python
import serial
import struct
import sys
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
            'enable', 'disable', 'pinmode', 'get_pinmode', 'enable_td',
            'disable_td', 'conf_td', 'dig_read', 'dig_write', 'dig_read_range',
            'dig_write_range', 'read', 'write', 'check_int']

    def _cmd(self, command, *args):
        self._connection.write(struct.pack(
            'BBB', self._commands.index(command),
            *(args + (0,) * (2 - len(args)))))

    def enable(self):
        self._cmd('enable')

    def disable(self):
        self._cmd('disable')

    def pinmode(self, pin, mode):
        self._cmd('pinmode', pin, mode)

    def get_pinmode(self, pin, mode):
        self._cmd('pinmode', pin)
        return ord(self._connection.read(1))

    def digital_read(self, pin):
        self._cmd('dig_read', pin)
        return ord(self._connection.read(1))

    def digital_write(self, pin, data):
        self._cmd('dig_write', pin, data)

    def digital_read_range(self, pin):
        self._cmd('dig_read_range', pin)
        return ord(self._connection.read(1))

    def digital_write_range(self, pin, data):
        self._cmd('dig_write_range', pin, data)

    def read(self, address):
        self._cmd('read', address)
        return ord(self._connection.read(1))

    def check_int(self):
        self._cmd('check_int')
        return ord(self._connection.read(1))

    def pulse(self, pin, duration):
        digital_write(pin, self.HIGH)
        time.sleep(duration)
        digital_write(pin, self.LOW)

    def dump(self):
        for address in range(0x60):
            data = max7301.read(address)
            sys.stdout.write(
                '0x{:02x}: 0x{:02x} 0b{:08b}\n'.format(address, data, data))


def main():
    max7301 = MAX7301()

    max7301.enable()
    max7301.pin_mode(12, MAX7301.INPUT_PULLUP)
    max7301.pin_mode(22, MAX7301.OUTPUT)

    max7301.pin_mode(31, MAX7301.OUTPUT)
    max7301.pin_mode(24, MAX7301.INPUT_PULLUP)
    max7301.conf_td(24, True)
    max7301.enable_td()

    max7301.digital_write(22, MAX7301.LOW)

    while True:
        if not max7301.digital_read(12):
            max7301.pulse(22, 0.2)

        if max7301.check_interrupt:
            max7301.pulse(22, 0.2)
            max7301.enable_td()

        time.sleep(1.0)


if __name__ == '__main__':
    main()
