"""
This module provides functions to help you to use a rotary encoder with push button.

The encoder's two inputs form a "Gray Code", where each step changes only one bit.
We can interpret the A and B inputs from the encoder as binary bits to form
an integer value. If we combine the new value and previous value we have
16 possible combinations. We create a lookup table for all possible inputs
now and previous scan to directly determine what the change should be.

 Previous  Now   Table  Change
   A B     A B   Index
 ------------------------------
   0 0     0 0     0      0
   0 0     0 1     1     -1
   0 0     1 0     2     +1
   0 0     1 1     3      *

   0 1     0 0     4     +1
   0 1     0 1     5      0
   0 1     1 0     6      *
   0 1     1 1     7     -1

   1 0     0 0     8     -1
   1 0     0 1     9      *
   1 0     1 0    10      0
   1 0     1 1    11     +1

   1 1     0 0    12      *
   1 1     0 1    13     +1
   1 1     1 0    14     -1
   1 1     1 1    15      0

* These positions are indeterminant. We can't tell if the direction is CW or CCW.
With some clever programming we could keep track of any velocity in the previous
change and assume two steps in the same direction. In practice it is difficult to
move the dial fast enough to ever skip steps do so we will just ignore the double
steps.
"""

from gpiozero import DigitalInputDevice, OutputDevice

# The GPIO pin numbers for the components of the rotary encoder.
encoder_a_pin = 17
encoder_b_pin = 27
button_pin = 22

# Table encapsulating all of the possible current and previous sensor inputs
# and the resulting delta to position.
result_table = [
   0, -1,  1,  2,
   1,  0,  2, -1,
  -1,  2,  0,  1,
   2,  1, -1,  0]

# Current position of the encoder.
position = 0

# Previous A and B sensor input values.
prev_a = 0
prev_b = 0


def create_encoder(pin):
  """
  Creates and configures a DigitialInputDevice at the specified pin for use
  as a rotary encoder input.

  This function is intended for internal use only.
  """
  encoder = DigitalInputDevice(pin, pull_up=True)
  encoder.when_activated = on_change
  encoder.when_deactivated = on_change
  return encoder


# Initialize the GPIO pins needed to read the keypad.
def init():
  """Initialize the GPIO pins needed to read a rotary encoder with push button."""
  global encoder_a, encoder_b, button
  encoder_a = create_encoder(encoder_a_pin)
  encoder_b = create_encoder(encoder_b_pin)
  button = DigitalInputDevice(button_pin, pull_up=False)


def on_change():
  """
  Inspect the rotary encoder A/B inputs and determine if the dial moved.

  This function is used internally to inspect the input pins when they changed.
  It is not intended to be called externally.
  """
  global position, prev_a, prev_b

  index = (prev_a<<3) | (prev_b<<2) | (encoder_a.value<<1) | (encoder_b.value)
  encoder_change = result_table[index]
  
  prev_a = encoder_a.value
  prev_b = encoder_b.value

  # For now, ignore the 2s. A value of 2 means we don't know if we're going forwards
  # or backwards. As an improvement we could keep track of the direction of the last change
  # and when we see a 2 adjust the sign accordingly and return +/-2.
  if encoder_change != 2:
    position = position + encoder_change


def get_position():
  """Return the current position of the rotary encoder."""
  global position
  return position


def set_position(value):
  """Set the current position of the rotary encoder.

  This function is useful for reseting the current physical position to a known
  logicial position (e.g. reset to zero).
  """
  global position
  position = value


def get_button_pressed():
  """Returns True if the button is currently pressed."""
  return button.value
