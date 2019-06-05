import mido
from mido import Message
import os
import time
#import mido.backends.rtmidi

print(mido.get_input_names())
print(mido.get_output_names()) 
outport = mido.open_output()
counter = 0
msg = mido.Message('note_on', note=100, velocity=80, channel=0)


print("Press q to quit")
while (counter < 9):


	
	print("Yo dawg")
	
	outport.send(msg.copy())
	time.sleep(2)
	outport.send(Message('note_off', note=100))
	counter+=1



	
	
											

