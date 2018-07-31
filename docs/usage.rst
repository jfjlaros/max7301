Usage
=====

In this section we describe how to configure and use the API library.

Configuration
-------------

Include the header file and make a global class instance, i.e., put it outside
of any function at the top of the sketch. The constructor of this class takes
five variables:

+------------+-------------------+----------------+
| position   | description       | abbreviation   |
+============+===================+================+
| 1          | clock pin         | CLK            |
+------------+-------------------+----------------+
| 2          | data in pin       | DIN            |
+------------+-------------------+----------------+
| 3          | data out pin      | DOUT           |
+------------+-------------------+----------------+
| 4          | chip select pin   | CS             |
+------------+-------------------+----------------+
| 5          | chip type         |                |
+------------+-------------------+----------------+

The chip type should be ``true`` for the MAX7301AAX, ``false`` otherwise.

+--------------+--------+-------------+
| type         | pins   | value       |
+==============+========+=============+
| MAX7301AAX   | 36     | ``true``    |
+--------------+--------+-------------+
| MAX7301ANI   | 28     | ``false``   |
+--------------+--------+-------------+
| MAX7301AAI   | 28     | ``false``   |
+--------------+--------+-------------+

If, for example, we have the clock, data in, data out and chip select on pins
4, 5, 6 and 7 respectively and our chip is of type MAX7301ANI, initialise the
class instance as follows:

.. code:: cpp

    #include <max7301.h>

    MAX7301 max7301(4, 5, 6, 7, false);

After initialisation, the MAX7301 is in shutdown mode. Use the ``enable()``
function to make it enter normal operation mode. This is typically done in the
``setup()`` function.

.. code:: cpp

    max7301.enable();

Pins can be configured by using the ``pinMode()`` function which takes the pin
number and a mode as arguments.

+-------------------------+------------------------------------+
| mode                    | description                        |
+=========================+====================================+
| ``GPIO_OUTPUT``         | logic output                       |
+-------------------------+------------------------------------+
| ``GPIO_INPUT``          | logic input                        |
+-------------------------+------------------------------------+
| ``GPIO_INPUT_PULLUP``   | logic input with internal pullup   |
+-------------------------+------------------------------------+

For example, configure pin 12 as an input with the internal pullup resistor
enabled and pin 22 as an output:

.. code:: cpp

    max7301.pinMode(12, GPIO_INPUT_PULLUP);
    max7301.pinMode(22, GPIO_OUTPUT);

The pin configuration can be queried with the ``getPinMode()`` function.

.. code:: cpp

    byte result = max7301.getPinMode(12); // Should return GPIO_INPUT_PULLUP.


Communication
-------------

The functions ``digitalRead()`` and ``digitalWrite()`` can be used to read from
a pin, or write to a pin.

.. code:: cpp

    byte result = max7301.digitalRead(12);
    max7301.digitalWrite(22, HIGH);

The functions ``digitalReadRange()`` and ``digitalWriteRange()`` can be used to
read from up to 8 consecutive pin at once. The first parameter indicates the
first pin in the range. The pin states are encoded in one byte with the pin
with the lowest number in its least significant position.

.. code:: cpp

    byte result = max7301.digitalReadRange(12); // Read pin 12-19.
    max7301.digitalWriteRange(22, 0x01);        // Set pin 22 HIGH and 23-29 LOW.


Shutdown
--------

The MAX7301 can be put in shutdown mode with the ``disable()`` function. In
this mode, all pins are set to input and the pullup resistors are turned off.

.. code:: cpp

    max7301.disable();


Transition detection
--------------------

The MAX7301 is capable of transition detection on pins 24 to 30. If a
transition is detected, pin 31 will go high.

To set this up, the pins must be configured correctly with the ``pinMode()``
function and the input pins must be registered for active monitoring with the
``configureTransitionDetection()`` function.

First make sure pin 31 is configured as an output pin.

.. code:: cpp

    max7301.pinMode(31, GPIO_OUTPUT);

To configure pin 24 as input:

.. code:: cpp

    max7301.pinMode(24, GPIO_INPUT);
    max7301.configureTransitionDetection(24, true);

Finally, activate transition detection with the ``enableTransitionDetection()``
function. This function must be called after every transition event to reenable
transition detection.

.. code:: cpp

    max7301.enableTransitionDetection();

Transition detection can be disabled with the ``disableTransitionDetection()``
function.


Low level functions
-------------------

Registers can be read with the ``read()`` function and written to with the
``write()`` function. The first parameter is the address of the register.

.. code:: cpp

    byte result = max7301.read(0x09); // First port configuration register.
    max7301.write(0x09, 0x55);        // Set port 4-7 to output.
