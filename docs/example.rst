Example sketch
==============

.. warning:: Under construction.

In this sketch_, we demonstrate the different capabilities of the MAX7301. We
connect two buttons and one LED.

- Button 1 is connected to a normal input pin (12).
- Button 2 is connected to an input pin with transition detection (24).

Both buttons drive an LED on pin 22, button 1 will simply turn the LED on when
pressed and button 2 will send a short pulse to the LED.

.. figure:: schema.svg
   :alt: Schema

   Schema for the test setup, see the MAX7301 datasheet_ for full installation
   instructions.

After compiling and uploading the sketch, connect the Arduino to a USB port and
run the host side script.

::

    python host.py


.. _sketch: https://github.com/jfjlaros/max7301/blob/master/device/src/device.ino
.. _datasheet: https://datasheets.maximintegrated.com/en/ds/MAX7301.pdf
