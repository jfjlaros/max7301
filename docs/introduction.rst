Introduction
============

    The MAX7301 compact, serial-interfaced I/O expander (or general-purpose I/O
    (GPIO) peripheral) provides microprocessors with up to 28 ports. Each port
    is individually user configurable to either a logic input or logic output.

    Each port can be configured either as a push-pull logic output capable of
    sinking 10mA and sourcing 4.5mA, or a Schmitt logic input with optional
    internal pullup. Seven ports feature configurable transition detection
    logic, which generates an interrupt upon change of port logic level. The
    MAX7301 is controlled through an SPI-compatible 4-wire serial interface.

    -- From the MAX7301 datasheet_.

This library provides an `API interface`_ to the MAX7301. Additionally, an
example_ sketch_ is included for serial communication with a host computer and an
example host script_ is included for controlling the MAX7301.


.. _datasheet: https://datasheets.maximintegrated.com/en/ds/MAX7301.pdf
.. _API interface: usage.html
.. _example: example.html
.. _sketch: https://github.com/jfjlaros/max7301/blob/master/device/src/device.ino
.. _script: https://github.com/jfjlaros/max7301/blob/master/host/host.py
