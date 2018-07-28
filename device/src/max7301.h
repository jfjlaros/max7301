#ifndef MAX7301_h
#define MAX7301_h

#include <Arduino.h>
#include <SPI.h>

#define NOP 0x00


class MAX7301 {
  public:
    MAX7301(int, int, int, int);
    void write(byte, byte);
    byte read(byte);
  private:
    byte _transfer(byte);
    int _pinCLK,
        _pinDIN,
        _pinDOUT,
        _pinCS;
};

#endif
