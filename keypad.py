"""
This module provides functions to help you to use a matrix keypad.
"""

from gpiozero import DigitalInputDevice, OutputDevice

# The character shown on each of the keys.
names = [
  ["1", "2", "3", "A"],
  ["4", "5", "6", "B"],
  ["7", "8", "9", "C"],
  ["*", "0", "#", "D"]]

rowCol = {
  "1": [0, 0],
  "2": [0, 1],
  "3": [0, 2],
  "A": [0, 3],
  "4": [1, 0],
  "5": [1, 1],
  "6": [1, 2],
  "B": [1, 3],
  "7": [2, 0],
  "8": [2, 1],
  "9": [2, 2],
  "C": [2, 3],
  "*": [3, 0],
  "0": [3, 1],
  "#": [3, 2],
  "D": [3, 3]
}




# The GPIO pin numbers for each row and column
#row_pins = [6, 13, 19, 26]
#col_pins = [12, 16, 20, 21]
row_pins = [2, 3, 4, 26]
col_pins = [14, 15, 23, 21]

# The objects representing the GPIO input/output pins.
row_gpios = []
col_gpios = []

def init():
  """Initialize the GPIO pins needed to read the keypad."""
  for pin in row_pins:
    device = OutputDevice(pin)
    row_gpios.append(device)

  for pin in col_pins:
    device = DigitalInputDevice(pin)
    col_gpios.append(device)


def scan():
  """Scan the keypad and return a list of the keys currently pressed."""
  keys = []

  # Enable each row one at a time.
  for row_index in range(len(row_gpios)):
    row = row_gpios[row_index]
    row.on()

    # Check each column to see if any keys on the row were pressed.
    for col_index in range(len(col_gpios)):
      col = col_gpios[col_index]
      if col.value:
        # Got one, record it.
        keys.append(names[row_index][col_index])
    row.off()

  return keys

