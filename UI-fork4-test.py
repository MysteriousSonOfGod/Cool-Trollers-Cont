from tkinter import *
from tkinter import messagebox
import configparser
import os.path
import mido
import os
import numpy as np
import pygame 
from msvcrt import getch

global lmao	
   #This function is what determines when to play which note from which button
#button_was_pressed is equal to 0 when it has gone two frames without being pressed.
#It is equal to 1 when it has gone one frame without being pressed.
#And equal to two when it is pressed.
def signalOnPress(note1, button1, lmao):
	global button
	i = lmao
	if button == 1 and i == button1 and button_was_pressed[i] ==0 and safeCheck1==1:
		outport.send(mido.Message('note_on', note=note1, velocity=100, channel=0))
		button_was_pressed[i] = 1
	elif button == 0 and i == button1 and button_was_pressed[i] ==1 and safeCheck2==1:
		outport.send(mido.Message('note_off', note=note1, velocity=100, channel=0))
		button_was_pressed[i] = 2
	elif button == 0 and i == button1 and button_was_pressed[i] ==2 and safeCheck2==1:
		button_was_pressed[i] = 0


#Loop until the user clicks the close button.
done = False
    
#This will be used for the dead zone on the controller sticks    
absolute_axis = 0

#This array holds the state of each button.
button_was_pressed = np.zeros(25)    

#This is used for pitch bend
pith=0

#These are used for debugging, making sure the code is reading the button inputs
Ding = "ding"
Dong = "dong"
		
safeCheck1=0
safeCheck2=0


# Main GUI class.
class GUI:
	def __init__(self, master):
	
		# Sets up main window.
		global window
		window = master
		master.title("Cooltrollers")
		#master.iconbitmap(default="controller.ico")
		
		# Adds menus.
		menuBar = Menu(master)
		fileMenu = Menu(menuBar, tearoff=0)
		optionsMenu = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Exit", command=quit)
		menuBar.add_cascade(label="Options", menu=optionsMenu)
		optionsMenu.add_command(label="Button Manager", command=self.buttonManager)
		master.config(menu=menuBar)
		
		# Sets up octave display. Every time it's changed via + or -, the display updates accordingly (via statements in functionality())
		global currentOctave
		global currentOctaveText
		currentOctave = 4
		currentOctaveText = StringVar()
		currentOctaveText.set("Current octave: %d" % currentOctave)
		octaveDisplay = Label(window, textvariable=currentOctaveText, anchor=NE)
		octaveDisplay.pack()
		
		
		# Initializes mido, the MIDI outport, and global variables that are used in functionality().
		# The amount of globals in the entire program is disgusting, but that'll be addressed later.
		print(mido.get_input_names())
		print(mido.get_output_names())
		global mido_out
		midi_out = mido.get_output_names()
		global outport
		outport = mido.open_output()
		
		global o_up
		global o_down
		global reset
		global octave
		global counter
		
		o_up = False
		o_down = False
		reset = False
		octave = 0
		counter = -1
		
		# Any key that's pressed activates functionality(), which plays notes.
		master.bind("<Key>", self.functionality)


	# buttonManager is the window that will allow users to bind keys for sound playback.
	def buttonManager(self):
	
		# Config file setup; may or may not keep.
		global config
		global bindCount
		if (os.path.isfile('settings.ini')):
			config.read('settings.ini')
			bindCount = config['Button Binds']['ButtonBindCount']
			bindCount = int(bindCount)
			#buttonBinds = config['Button Binds']['Binds'] -- put this somewhere else
		else:
			bindCount = 0
			#buttonBinds = [None]*32
			config['Button Binds'] = {'ButtonBindCount':0}
			with open('settings.ini', 'w') as configfile:
				config.write(configfile)
		
		# Window setup.
		global window
		global buttonMgr
		buttonMgr = Toplevel(window)
		buttonMgr.grab_set()
		buttonMgr.focus_set()
		buttonMgr.maxsize()
		buttonMgr.title("Button Manager")
		
		# buttonFrame setup.
		global buttonFrame
		buttonFrame = Frame(buttonMgr)
		buttonFrame.pack(fill=BOTH, expand=YES)
		addBind = Button(buttonFrame, text="Add", width=25, command=self.buttonBinding)
		addBind.pack()
		removeBind = Button(buttonFrame, text="Delete", width=25, command=self.bindDelete)
		removeBind.pack()
		
		# Loading button binds onto screen.
		global box
		global canvas
		box = [None]*16
		canvas = Canvas(buttonFrame, width=150, height=470)
		canvas.pack()
		for x in range(bindCount):
			box[x-1] = canvas.create_rectangle(0, 30*(x-1), 149, (30*x)-1, fill="white", outline="")

	# Adds button binds. 16 maximum.
	def buttonBinding(self):
		global buttonMgr
		global bindCount
		global box
		global canvas
		if (bindCount < 16):
			box[bindCount-1] = canvas.create_rectangle(0, 30*(bindCount-1), 149, (30*bindCount)-1, fill="white", outline="")
			bindCount += 1
			buttonMgr.geometry=("200x%s" % str((30*bindCount)+30))
			with open('settings.ini', 'w') as configfile:
				config['Button Binds'] = {'ButtonBindCount':bindCount}
				config.write(configfile)		
		else:
			messagebox.showinfo("Bind Limit Exceeded", "You may only have 16 binds at maximum.")
	
	# Deletes button binds.
	def bindDelete(self):
		global bindCount
		global buttonMgr
		global box
		global canvas
		
		if (bindCount > 0):
			canvas.delete(box[bindCount-1])
			bindCount -= 1
			buttonMgr.geometry=("200x%s" % str((30*bindCount)+30))
			
			with open('settings.ini', 'w') as configfile:
				config['Button Binds'] = {'ButtonBindCount':bindCount}
				config.write(configfile)

				
	# Plays back notes.
	def functionality(self, event):
		global mido_out
		global outport
		global o_up
		global o_down
		global reset
		global octave
		global counter
		global currentOctave
		global currentOctaveText

		key_on = event.char

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

		if (o_up == True and octave + 84 < 127):
			octave += 12
			currentOctave += 1
			currentOctaveText.set("Current octave: %d" % currentOctave)
		elif (o_up == False):
			octave = octave
		if (o_down == True and octave - 84 > -127):
			octave -= 12
			currentOctave -= 1
			currentOctaveText.set("Current octave: %d" % currentOctave)
		elif (o_down == False):
			octave = octave	 	

		if (reset):	
			octave = 0			
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



	  
	#Starts pygame
	pygame.init()
	 
	 # Used to manage how fast the screen updates
	clock = pygame.time.Clock()

	# Initialize the joysticks
	pygame.joystick.init()
	# -------- Main Program Loop -----------
	while done==False:
	    # EVENT PROCESSING STEP
	    for event in pygame.event.get(): # User did something
	        if event.type == pygame.QUIT: # If user clicked close
	            done=True # Flag that we are done so we exit this loop
	        
	        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION

	        #Here's the debugging events
	        if event.type == pygame.JOYBUTTONDOWN:
	            print(Ding)
	            safeCheck1=1
	            safeCheck2=0
	        if event.type == pygame.JOYBUTTONUP:
	            print(Dong)
	            safeCheck1=0
	            safeCheck2=1
	            
	 
	    # DRAWING STEP
	    # First, clear the screen to white. Don't put other drawing commands
	    # above this, or they will be erased with this command.

	    # Get count of joysticks
	    joystick_count = pygame.joystick.get_count()
	    
	    # For each joystick:
	    for i in range(joystick_count):
	        joystick = pygame.joystick.Joystick(i)
	        joystick.init()
	    
	    
	        # Get the name from the OS for the controller/joystick
	        name = joystick.get_name()
	        
	        # Usually axis run in pairs, up/down for one, and left/right for
	        # the other.
	        axes = joystick.get_numaxes()

	        
	         
	        #pitch bend
	        for i in range( axes ):
	            
	            axis = joystick.get_axis( i )
	            if axis < 0:
	                absolute_axis = axis*-1
	            else:
	                absolute_axis = axis

	            if i == 1 and (absolute_axis*8000 > 250):
	                pith = -8000*axis
	                outport.send(mido.Message('pitchwheel', pitch = int(pith)))
	           
	        buttons = joystick.get_numbuttons()
	        
	        #Here are the button mappings and the playing of the notes
	        for i in range(buttons):
	        	global button
	        	lmao = i
	        	button = joystick.get_button( i )
	        	signalOnPress(62, 0, lmao)
	        	signalOnPress(69, 1, lmao)
	        	signalOnPress(64, 2, lmao)
	        	signalOnPress(72, 3, lmao)
	        	signalOnPress(69, 4, lmao)
	        	signalOnPress(74, 5, lmao)                                                                         

	            #if button == 1 and i==1:
	                #outport.send(mido.Message('control_change', value=100))    

	        # Hat switch. All or nothing for direction, not like joysticks.
	        # Value comes back in an array.
	        hats = joystick.get_numhats()

	        for i in range( hats ):
	            hat = joystick.get_hat( i )

	    
	    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
	    
	    # Go ahead and update the screen with what we've drawn.


	    # Limit to 20 frames per second
	    clock.tick(240)

	    #outport.reset()
    


# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.



	
					

root = Tk()
global config
config = configparser.ConfigParser()
prog = GUI(root)
root.mainloop()
pygame.quit ()