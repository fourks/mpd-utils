'''
Work around for the lack of MPD218 driver in MPC Essentials, many
functions within DAW do not support control via MIDI notes.

This python script detects notes (from MPC preset, BankC) and issue
keyboard presses to the active window, which do drive the functions
within MPC Essentials

It 'shims' between MPD218 and MPC essentials, relaying the Midi and
keypresses. The keypresses are only detected from BankC enable user
to easily enable/disable.

Requires:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtmidi-python
https://github.com/olemb/mido
https://github.com/boppreh/keyboard

Setup:
Install the above, or use the pre-built binary

Install the 'Akai Internal MIDI Port' located within MPC directory
C:\Program Files\Akai Pro\MPC Essentials\support

In MPC Essentials, under Edit/Preferences/Midi set a Midi-Output 
to 'Akai Internal MIDI'.

Run script/exe in command window and then switch back to MPC
'''
import sys
import mido
import keyboard

print("MPD218 Pads to Keys - midi notes to key presses")
inport = None

mido.set_backend('mido.backends.rtmidi_python')
print(mido.get_input_names())

for port in mido.get_input_names():
  if port[:6]==b'MPD218':
    inport = port
    print("Using:", inport)
    break

if inport == None:
  sys.exit("Unable to find MPD218")

for port in mido.get_output_names():
  if port[:7]==b'AkaiPro':
    outport = mido.open_output(port)
    print("Relay:", port)
    break

if outport == None:
  sys.exit("Unable to find AkaiPro Midi Port")

with mido.open_input(inport) as port:
  for message in port:
    note_on=False
    key=None
    if message.channel !=9:
      outport.send(message)
      continue
    if message.type=='note_on':
      note_on=True
    if message.type=='note_on' or message.type=='note_off':
      if message.note==52:
        key = 'z'
      if message.note==57:
        key = 'x'
      if message.note==58:
        key = 'c'
      if message.note==59:
        key = 'v'

      if message.note==60:
        key = 'a'
      if message.note==61:
        key = 's'
      if message.note==67:
        key = 'd'
      if message.note==68:
        key = 'f'

      if message.note==70:
        key = 'q'
      if message.note==72:
        key = 'w'
      if message.note==75:
        key = 'e'
      if message.note==78:
        key = 'r'

      if message.note==79:
        key = '1'
      if message.note==35:
        key = '2'
      if message.note==41:
        key = '3'
      if message.note==50:
        key = '4'

    if key:
      if note_on:
        keyboard.press(key)
      else:
        keyboard.release(key)
    else:
      outport.send(message)
