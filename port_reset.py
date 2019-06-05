import mido
import os
import time
import mido.backends.rtmidi

print(mido.get_input_names())
print(mido.get_output_names()) 
outport = mido.open_output("lport 3")
outport.reset()





	
	
											

