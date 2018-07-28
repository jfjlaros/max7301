#ifndef MAX7301_h
#define MAX7301_h

#include <Arduino.h>

#define NOP 0x00
#define GPIO_OUTPUT 0x01
#define GPIO_INPUT 0x02
#define GPIO_INPUT_PULLUP 0x03


class MAX7301 {
  public:
    MAX7301(int, int, int, int, bool);
    byte read(byte),
         getPinMode(byte),
         digitalRead(byte);
    void write(byte, byte),
         enable(void),
         disable(void),
         pinMode(byte, byte),
         digitalWrite(byte, byte);
  private:
    byte _transfer(byte);
    int _pinCLK,
        _pinDIN,
        _pinDOUT,
        _pinCS;
};

#endif
