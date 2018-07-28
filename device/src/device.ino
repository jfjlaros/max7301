/* MAXIM 7301 port I/O expander. */
#include "max7301.h"

MAX7301 max7301(2, 3, 4, 5, false);


void setup(void) {
  max7301.enable();
  max7301.pinMode(12, GPIO_INPUT_PULLUP);
  max7301.pinMode(22, GPIO_OUTPUT);

  Serial.begin(0x9600);
}

void loop(void) {
  static byte led = LOW;

  if (Serial.available()) {
    Serial.println(max7301.digitalRead(12));
  }
  if (!max7301.digitalRead(12)) {
    max7301.digitalWrite(22, led);
    led = !led;
  }
  else {
    max7301.digitalWrite(22, LOW);
  }
  delay(500);
}
