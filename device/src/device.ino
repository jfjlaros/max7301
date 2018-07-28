/* MAXIM 7301 port I/O expander. */
#include "max7301.h"

MAX7301 max7301(2, 4, 3, 5);


void setup(void) {
  max7301.write(0x04, 0x01);
  max7301.write(0x09, 0x55);

  Serial.begin(0x9600);
}

void loop(void) {
  if (Serial.available()) {
    Serial.println(max7301.read(0x09), HEX);
  }
  delay(1000);
}
