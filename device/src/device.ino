#include <max7301.h>

#define CMD_ENABLE 0x00
#define CMD_DISABLE 0x01
#define CMD_PINMODE 0x02
#define CMD_GET_PINMODE 0x03
#define CMD_ENABLE_TD 0x04
#define CMD_DISABLE_TD 0x05
#define CMD_CONF_TD 0x06
#define CMD_DIG_READ 0x07
#define CMD_DIG_WRITE 0x08
#define CMD_DIG_READ_RANGE 0x09
#define CMD_DIG_WRITE_RANGE 0x0a
#define CMD_READ 0x0b
#define CMD_WRITE 0x0c
#define CMD_CHECK_INT 0x0d

MAX7301 max7301(4, 5, 6, 7, false);
volatile bool button_change = false;


void button_interrupt(void) {
  button_change = true;
}


void setup(void) {
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(1, button_interrupt, RISING);

  Serial.begin(9600);
}

void loop(void) {
  char cmd[3];

  if (Serial.available()) {
    Serial.readBytes(cmd, 3);

    switch (cmd[0]) {
      case CMD_ENABLE:
        max7301.enable();
        break;
      case CMD_DISABLE:
        max7301.disable();
        break;
      case CMD_PINMODE:
        max7301.pinMode((byte)cmd[1], (byte)cmd[2]);
        break;
      case CMD_GET_PINMODE:
        Serial.write(max7301.getPinMode((byte)cmd[1]));
        break;
      case CMD_ENABLE_TD:
        max7301.enableTransitionDetection();
        button_change = false;
        break;
      case CMD_DISABLE_TD:
        max7301.disableTransitionDetection();
        break;
      case CMD_CONF_TD:
        max7301.configureTransitionDetection((byte)cmd[1], (bool)cmd[2]);
        break;
      case CMD_DIG_READ:
        Serial.write(max7301.digitalRead((byte)cmd[1]));
        break;
      case CMD_DIG_WRITE:
        max7301.digitalWrite((byte)cmd[1], (byte)cmd[2]);
        break;
      case CMD_DIG_READ_RANGE:
        Serial.write(max7301.digitalReadRange((byte)cmd[1]));
        break;
      case CMD_DIG_WRITE_RANGE:
        max7301.digitalWriteRange((byte)cmd[1], (byte)cmd[2]);
        break;
      case CMD_READ:
        Serial.write(max7301.read((byte)cmd[1]));
        break;
      case CMD_WRITE:
        max7301.write((byte)cmd[1], (byte)cmd[2]);
        break;
      case CMD_CHECK_INT:
        Serial.write((byte)button_change);
        break;
    }
  }
}
