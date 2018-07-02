/* MAXIM 7310 port I/O expander. */

// LED pin.
#define LED_PIN 13

// LED blink durations.
#define LED_SHORT 100
#define LED_LONG 500


void blink(int duration) {
  digitalWrite(LED_PIN, HIGH);
  delay(duration);
  digitalWrite(LED_PIN, LOW);
}

void signal(byte data) {
  int i;

  for (i = 7; i >= 0; i--) {
    if (data & (1 << i)) {
      blink(LED_LONG);
    }
    else {
      blink(LED_SHORT);
    }
    delay(LED_SHORT);
  }
}


void setup(void) {
  pinMode(LED_PIN, OUTPUT);
}

void loop(void) {
}
