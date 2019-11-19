#!/usr/bin/python3

"""
Motor control test software for use with the Spark Max motor controller.
"""

import argparse
import datetime
import time
import pprint

from guizero import App, Box, Slider, Text

import keypad
import rotary_encoder

current_key = 0
keys = []

def gui_loop(text, slider):
  """
  This function is called repeatedly by the GUI event loop.
  """

  # Check the position of the rotary encoder and report new values.
  rot_position = rotary_encoder.get_position()
  slider.value = rot_position/4 % 100

  # Reset key press indicators
  for row in range(4):
    for col in range(4):
      keys[row][col].bg = "gray"
      keys[row][col].text_color = "black"

  new_keys = keypad.scan()
  for current_key in new_keys:
    # Map key character to number
    r,c = keypad.rowCol[current_key]
    key = keys[r][c]
    key.bg = "black"
    key.text_color = "white"


def main():
  """
  Main function of the program. This main function will choose to run either text_main
  or gui_main depending on the command line arguments.
  """

  parser = argparse.ArgumentParser(description="SparkMax Motor Controller Interface")
  parser.add_argument("-t", "--textonly", action="store_true",
    help="No GUI, text only interface")
  args = parser.parse_args()
  if args.textonly:
    text_main()
  else:
    gui_main()


def gui_main():
  """
  The main function for GUI mode. This function sets up the GUI elements
  and launches the GUI event loop.
  """
  app = App(title="Nikola", bg="black")

  text = Text(app, color="light sky blue")
  text.text_size = 36

  keybox = Box(app, layout="grid", border=3)
  keybox.text_color = "white"
  keybox.bg = "gray"
  for row in range(4):
    keys.append([])
    for col in range(4):
      key = Text(keybox, grid=[col,row], text=keypad.names[row][col], size=24)
      keys[row].append(key)

  slider = Slider(app, height=36, width="fill", end=100)
  slider.bg = "blue"
  slider.text_color = "white"

  app.repeat(100, gui_loop, args=[text, slider])

  keypad.init()
  rotary_encoder.init()

  app.set_full_screen()
  app.display()


def text_main():
  """
  The main function for text-only mode. This function sets up the keypad
  and rotary encoder inputs and then enters a loop monitoring the inputs
  and reporting status the standard out.
  """

  # Initialize the inputs.
  print("Text only mode")
  keypad.init()
  rotary_encoder.init()

  # Prepare state variables.
  prev_keys = []
  prev_position = 999
  prev_button = False

  # Event loop.
  while True:
    # Look for and report changes (key up or down) on the keypad.
    new_keys = keypad.scan()
    if prev_keys != new_keys:
      print("Keypad = [%s]" % (",".join(new_keys)))
      prev_keys = new_keys

    # Check the position of the rotary encoder and report new values.
    new_position = rotary_encoder.get_position()
    if prev_position != new_position:
      print("Rotary encoder position = %d" % new_position)
      prev_position = new_position

    # Check the button on the rotary encoder and report changes. If pressed,
    # reset the rotary encoder position to zero.
    new_button = rotary_encoder.get_button_pressed()
    if prev_button != new_button:
      if new_button:
        rotary_encoder.set_position(0)
        print("Button pressed")
      else:
        print("Button released")
      prev_button = new_button

    # Take a short nap before doing it all again.
    time.sleep(0.010)


if __name__ == "__main__":
  main()

