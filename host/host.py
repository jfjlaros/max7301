#!/usr/bin/env python
import serial
import struct
import sys
import time


OUTPUT = 0x01
INPUT = 0x02
INPUT_PULLUP = 0x03
LOW = 0x00
HIGH = 0x01


class MAX7301(object):
    """Simple serial interface for the MAX7301."""

    def __init__(self):
        """Initialise the interface."""
        self._connection = serial.Serial('/dev/ttyACM0')
        self._commands = [
            'enable', 'disable', 'pinmode', 'get_pinmode', 'enable_td',
            'disable_td', 'conf_td', 'dig_read', 'dig_write', 'dig_read_range',
            'dig_write_range', 'read', 'write', 'check_int']
        self._byte_commands = [
            'get_pinmode', 'dig_read', 'dig_read_range', 'read', 'check_int']

    def cmd(self, command, *args):
        """Send a command to the serial connection.

        :arg str command: MAX7301 command.
        :arg list *args: Parameters for {command}.
        :arg bool result: When True, read one byte from the serial connection.

        :returns any: Either the result of {command} or None.
        """
        self._connection.write(struct.pack(
            'BBB', self._commands.index(command),
            *(args + (0,) * (2 - len(args)))))

        if command in self._byte_commands:
            return struct.unpack('B', self._connection.read(1))[0]
        return None

    def pulse(self, pin, up, down):
        """Send a short pulse to a pin.

        :arg int pin: Pin number.
        :arg float up: Pin high duration.
        :arg float down: Pin low duration.
        """
        self.cmd('dig_write', pin, HIGH)
        time.sleep(up)
        self.cmd('dig_write', pin, LOW)
        time.sleep(down)

    def dump(self):
        """Dump all registers of the MAX7301 to standard output."""
        for address in range(0x60):
            data = self.cmd('read', address)
            sys.stdout.write(
                '0x{:02x}: 0x{:02x} 0b{:08b}\n'.format(address, data, data))


def main():
    max7301 = MAX7301()

    max7301.cmd('enable')
    max7301.cmd('pinmode', 12, INPUT_PULLUP)
    max7301.cmd('pinmode', 22, OUTPUT)

    max7301.cmd('pinmode', 31, OUTPUT)
    max7301.cmd('pinmode', 24, INPUT_PULLUP)
    max7301.cmd('conf_td', 24, True)
    max7301.cmd('enable_td')

    max7301.cmd('dig_write', 22, LOW)

    while True:
        if not max7301.cmd('dig_read', 12):
            max7301.pulse(22, 0.01, 0.05)

        if max7301.cmd('check_int'):
            for _ in range(3):
                max7301.pulse(22, 0.01, 0.05)
            max7301.cmd('enable_td')

        time.sleep(1.0)


if __name__ == '__main__':
    main()
