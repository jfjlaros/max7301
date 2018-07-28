#include "max7301.h"


/**
 * Constructor.
 *
 * @arg {int} pinCLK - Clock pin.
 * @arg {int} pinDIN - Data In pin.
 * @arg {int} pinDOUT - Data Out pin.
 * @arg {int} pinCS - Chip select pin.
 */
MAX7301::MAX7301(int pinCLK, int pinDIN, int pinDOUT, int pinCS) {
  _pinCLK = pinCLK;
  _pinDIN = pinDIN;
  _pinDOUT = pinDOUT;
  _pinCS = pinCS;

  pinMode(_pinCLK, OUTPUT);
  pinMode(_pinDIN, OUTPUT);
  pinMode(_pinDOUT, INPUT_PULLUP);
  pinMode(_pinCS, OUTPUT);
}

/**
 * Write one byte to DIN, read one byte from DOUT.
 *
 * @arg {byte} data - Data.
 *
 * @return {byte} - Result.
 */
byte MAX7301::_transfer(byte data) {
  byte result = 0x00;
  int bit;

  for (bit = 7; bit >= 0; bit--) {
    digitalWrite(_pinCLK, LOW);
    digitalWrite(_pinDIN, data & (0x01 << bit));
    result |= digitalRead(_pinDOUT) << bit;
    digitalWrite(_pinCLK, HIGH);
  }
  digitalWrite(_pinCLK, LOW);

  return result;
}

/**
 * Write one byte to the specified addres.
 *
 * @arg {byte} address - Address.
 * @arg {byte} data - Data.
 */
void MAX7301::write(byte address, byte data) { 
  digitalWrite(_pinCS, LOW);
  _transfer(address & ~0x80);
  _transfer(data);
  digitalWrite(_pinCS, HIGH);
}

/**
 * Read one byte from the specified addres.
 *
 * @arg {byte} address - Address.
 *
 * @return {byte} - Data.
 */
byte MAX7301::read(byte address) {
  byte result;

  digitalWrite(_pinCS, LOW);
  _transfer(address | 0x80);
  _transfer(NOP);
  digitalWrite(_pinCS, HIGH);

  digitalWrite(_pinCS, LOW);
  _transfer(NOP);
  result |= _transfer(NOP);
  digitalWrite(_pinCS, HIGH);

  return(result);
}
