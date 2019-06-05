import mido
import os
from pygame import pypm
from msvcrt import getch

o_up = False
o_down = False
reset = False
octave = 0
counter = -1
print(mido.get_input_names())
print(mido.get_output_names())
outport = mido.open_output('Microsoft MIDI Mapper') 

print("Hello! Press the buttons starting at the letter a on your keyboard as if it was a piano starting at middle c. Press + to bring everything an octave up, and press - to bring it an octave down.")
while (True):


	key_on = chr(ord(getch()))

	if (key_on == "+"):
		o_up = True
		o_down = False
	elif (key_on == "-"):
		o_down = True
		o_up = False
	elif (key_on == "*"):
		reset = True
	else:
		reset = False	

	if (o_up == True):
		octave += 12
	elif (o_up == False):
		octave = octave
	if (o_down == True):
		octave += -12
	elif (o_down == False):
		octave = octave	 	

	if (reset):	
		octave = 0			

	if (key_on == "q"):
		outport.send(mido.Message('note_off', note=(60+octave), velocity=80))
		outport.close
		break

	elif (key_on == "a"):
		outport.send(mido.Message('note_on', note=60+octave, velocity=80))
		
						
	elif (key_on == "w"):
		outport.send(mido.Message('note_on', note=61+octave, velocity=80))
		outport.close
		
	elif (key_on == "s"):
		outport.send(mido.Message('note_on', note=62+octave, velocity=80))
		outport.close
		
	elif (key_on == "e"):
		outport.send(mido.Message('note_on', note=63+octave, velocity=80))
		outport.close
		
	elif (key_on == "d"):
		outport.send(mido.Message('note_on', note=64+octave, velocity=80))
		outport.close
		
	elif (key_on == "f"):
		outport.send(mido.Message('note_on', note=65+octave, velocity=80))
		outport.close
		
	elif (key_on == "t"):
		outport.send(mido.Message('note_on', note=66+octave, velocity=80))
		outport.close
		
	elif (key_on == "g"):
		outport.send(mido.Message('note_on', note=67+octave, velocity=80))
		outport.close
		
	elif (key_on == "y"):
		outport.send(mido.Message('note_on', note=68+octave, velocity=80))
		outport.close
		
	elif (key_on == "h"):
		outport.send(mido.Message('note_on', note=69+octave, velocity=80))
		outport.close

	elif (key_on == "u"):
		outport.send(mido.Message('note_on', note=70+octave, velocity=80))
		outport.close

	elif (key_on == "j"):
		outport.send(mido.Message('note_on', note=71+octave, velocity=80))
		outport.close

	elif (key_on == "k"):
		outport.send(mido.Message('note_on', note=72+octave, velocity=80))
		outport.close

	counter = counter + 1
	if (counter % 2 == 0):		
		o_up = False
		o_down = False
		reset = False
	if (counter == 100):
		counter = 0			
											

