from tkinter import *
from tkinter import messagebox
import configparser
import os.path
import mido
import os
#import mido.backends.rtmidi
from pygame import pypm
from msvcrt import getch

# buttonManager is the window that will allow users to bind keys for sound playback.
# Keybinds will be saved to a local configuration file.
class GUI:
	def __init__(self, master):
		global window
		window = master
		master.title("Cooltrollers")
		#master.iconbitmap(default="controller.ico")
		menuBar = Menu(master)
		fileMenu = Menu(menuBar, tearoff=0)
		optionsMenu = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Sound Playback", command=self.soundPlay)
		fileMenu.add_command(label="Exit", command=quit)
		menuBar.add_cascade(label="Options", menu=optionsMenu)
		optionsMenu.add_command(label="Button Manager", command=self.buttonManager)
		master.config(menu=menuBar)

		
	def buttonManager(self):
		# Config file setup
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
			config['Button Binds'] = {'ButtonBindCount':0, 'Binds':buttonBinds}
			with open('settings.ini', 'w') as configfile:
				config.write(configfile)
		
		# Window opening
		global window
		global buttonMgr
		buttonMgr = Toplevel(window)
		buttonMgr.grab_set()
		buttonMgr.focus_set()
		#buttonMgr.resizable(0,0)
		buttonMgr.maxsize()
		buttonMgr.title("Button Manager")
		
		# buttonFrame setup
		global buttonFrame
		buttonFrame = Frame(buttonMgr)
		buttonFrame.pack(fill=BOTH, expand=YES)
		addBind = Button(buttonFrame, text="Add", width=25, command=self.buttonBinding)
		addBind.pack()
		removeBind = Button(buttonFrame, text="Delete", width=25, command=self.bindDelete)
		removeBind.pack()
		
		# Loading button binds onto screen
		global box
		global canvas
		box = [None]*16
		canvas = Canvas(buttonFrame, width=150, height=470)
		canvas.pack()
		for x in range(bindCount):
			box[x-1] = canvas.create_rectangle(0, 30*(x-1), 149, (30*x)-1, fill="white", outline="")
			
	def buttonBinding(self): # 16 MAXIMUM BINDS
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
				
	def soundPlay(self):
		global window
		soundPlay = Toplevel(window)
		
		#soundPlay.resizable(0,0)
		soundPlay.maxsize()
		soundPlay.title("Sound Playback")
		
		soundFrame = Frame(soundPlay, width=50, height=50, relief=SUNKEN)
		soundFrame.pack(fill=BOTH, expand=YES)

		soundFrame.focus_set()
		
		soundFrame.bind("<Key>", self.functionality)
		
		
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

	def functionality(self, event):
		global mido_out
		global outport
		global o_up
		global o_down
		global reset
		global octave
		global counter
		
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
		elif (o_up == False):
			octave = octave
		if (o_down == True and octave - 84 > -127):
			octave += -12
		elif (o_down == False):
			octave = octave	 	

		if (reset):	
			octave = 0			

		#if (key_on == "q"):
		#	outport.send(mido.Message('note_off', note=(60+octave), velocity=80))
		#	outport.close
		#	break

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
					
	
	
root = Tk()
global config
config = configparser.ConfigParser()
prog = GUI(root)
root.mainloop()