#!/usr/bin/env python
import serial
import struct
import time


class MAX7301(object):
    def __init__(self):
        self._connection = serial.Serial('/dev/ttyACM0')
        self._commands = [
            'enable', 'disable', 'pinmode', 'get_pinmode', 'conf_td',
            'enable_td', 'dig_read', 'dig_write', 'read', 'write']
        self._modes = ['', 'output', 'input', 'input_pullup']
        self._values = ['low', 'high']

    def cmd(self, command, *args):
        self._connection.write(struct.pack(
            'BBB', self._commands.index(command),
            *(args + (0,) * (2 - len(args)))))

    def pin_mode(self, pin, mode):
        self.cmd('pinmode', pin, self._modes.index(mode))

    def digital_read(self, pin):
        self.cmd('dig_read', pin)

        return ord(self._connection.read(1))

    def digital_write(self, pin, data):
        self.cmd('dig_write', pin, self._values.index(data))

    def read(self, address):
        self.cmd('read', address)

        return ord(self._connection.read(1))


def main():
    max7301 = MAX7301()

    max7301.cmd('enable')
    max7301.pin_mode(12, 'input_pullup')
    max7301.pin_mode(22, 'output')

    max7301.pin_mode(31, 'output')
    max7301.pin_mode(24, 'input_pullup')
    max7301.cmd('conf_td', 24, True)
    max7301.cmd('enable_td')

    for address in range(0x60):
        data = max7301.read(address)
        print '0x{:02x}: 0x{:02x} 0b{:08b}'.format(address, data, data)

    while True:
        if not max7301.digital_read(12):
            max7301.digital_write(22, 'high')
            time.sleep(0.5)
            max7301.digital_write(22, 'low')
        else:
            max7301.digital_write(22, 'low')
        time.sleep(0.5)

        max7301.cmd('enable_td')


if __name__ == '__main__':
    main()
