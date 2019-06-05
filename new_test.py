import time
import mido
import pygame
from mido import Message
import mido.backends.rtmidi


mido.set_backend('mido.backends.rtmidi')

print(mido.get_output_names())
 
port = mido.open_output("lport 3")
 
for note in range(60, 85):
    print(note)
    port.send(Message('note_on', note=note, velocity=100, channel=1))
    time.sleep(0.1)
    port.send(Message('note_off', note=note, velocity=100, channel=1))
    time.sleep(0.1)
    port.reset()