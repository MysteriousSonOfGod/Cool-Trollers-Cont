from tkinter import *
from tkinter import messagebox
import configparser
import os.path
import mido
import os
from pygame import pypm
from msvcrt import getch


# Main GUI class.
class GUI:
	def __init__(self, master):
		# Sets up main window.
		self.window = master
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
		master.resizable(0,0)
		
		# Initializes mido, the MIDI outport, and global variables that are used in functionality().
		midi_out = mido.get_output_names()
		self.octave = 0
		self.counter = -1
		
		# Sets up octave display. Every time it's changed via + or -, the display updates accordingly (via statements in functionality())
		self.currentOctaveText = StringVar()
		self.currentOctaveText.set("Current octave: {0}".format(int((self.octave/12)+4)))
		octaveDisplay = Label(master, textvariable=self.currentOctaveText, anchor=NE)
		octaveDisplay.grid(row=0)
		
		# Any key that's pressed activates functionality(), which plays notes.
		master.bind("<Key>", self.functionality)
		
		# Combo box and apply button for selecting MIDI port.
		self.port = StringVar(master)
		self.port.set(midi_out[0])
		self.currentPort = self.port
		portSelect = OptionMenu(master, self.port, *midi_out)
		portSelect.grid(row=1)
		applyPortButton = Button(master, text="Apply", command=self.applyPort)
		applyPortButton.grid(row=1, column=1)
		self.outport = mido.open_output(self.currentPort.get())
		
	# Uses an apply button to change output MIDI port.
	def applyPort(self):
		self.currentPort = self.port
		self.outport.close()
		self.outport = mido.open_output(self.currentPort.get())
		
		#self.outport.send(mido.Message('program_change', program=28))

	
	# buttonManager is the window that will allow users to bind keys for sound playback.
	def buttonManager(self):
		global config
		
		# Config file setup/reading. Uses strings with commas separating list items to store in the file.
		if (os.path.isfile('settings.ini')):
			config.read('settings.ini')
			keyString = config.get('Button Binds','Keys')
			instrumentString = config.get('Button Binds', 'Instruments')
			toneString = config.get('Button Binds', 'Tones')
			
			self.key = keyString.split(",")
			self.instrument = instrumentString.split(",")
			self.tone = toneString.split(",")
			
			for x in range(16):
				self.instrument[x] = int(self.instrument[x])
				self.tone[x] = int(self.tone[x])
				
		else:
			self.key = ["Empty"]*16
			self.instrument = [0]*16
			self.tone = [0]*16
			keyString = ""
			instrumentString = ""
			toneString = ""
			for x in range(16):
				keyString += (self.key[x] + ",") 
				instrumentString += (str(self.instrument[x]) + ",") 
				toneString += (str(self.tone[x]) + ",") 
				config['Button Binds'] = {'Keys':keyString, 'Instruments':instrumentString, 'Tones':toneString}
			with open('settings.ini', 'w') as configfile:
				config.write(configfile)
		
		# Window setup.
		self.buttonMgr = Toplevel(self.window)
		self.buttonMgr.grab_set()
		self.buttonMgr.focus_set()
		self.buttonMgr.title("Button Manager")
		self.buttonMgr.resizable(0,0)
		
		# Sets up text label for binding instructions.
		#instructions = Label(buttonMgr, text="Click a note and then press any key to bind that key to the given note.")
		#instructions.grid()
		
		# Sets up sixteen buttons for binding keys.
		r = 0
		c = 0
		self.bind=[None]*16
		button=[None]*16
		lengthTest = ""
		for x in range(16):
			self.bind[x] = StringVar()
			self.bind[x].set("Key: {0} \n Instrument: {1} \n Tone: {2}".format(self.key[x], self.instrument[x], self.tone[x]))
			button[x] = Button(self.buttonMgr, textvariable=self.bind[x], command=lambda: self.binding(self.key[x], self.instrument[x], self.tone[x], x))
			lengthTest += " "
			c += 1
			if (x % 4 == 0):
				r += 1
				c = 0
			button[x].grid(row=r, column=c)
	
	# Window that opens for every bind clicked for configuration.
	def binding(self, key, instr, tone, num):
		self.bindWindow = Toplevel(self.buttonMgr)
		self.bindWindow.title("Bind Configuration")
		self.bindWindow.focus_set()
		
		self.keyBindDisplay = StringVar()
		self.keyBindDisplay.set(key)
		self.newKey=key
		keyBind = Button(self.bindWindow, textvariable=self.keyBindDisplay, command=self.press_key)
		keyBind.grid(row=0)
		
		buttonOK = Button(self.bindWindow, text="OK", command=lambda:self.bindOK(num))
		buttonCancel = Button(self.bindWindow, text="Cancel", command=self.bindCancel)
		buttonOK.grid(row=4)
	
	def press_key(self):
		self.keyBindDisplay.set("Press any key...")
		self.bindWindow.bind("<Key>", self.key_bound)
		
	def key_bound(self, event):
		self.newKey = event.char
		self.keyBindDisplay.set(self.newKey)
		self.bindWindow.unbind("<Key>")
		
	def bindOK(self, num):
		self.key[num] = self.newKey
		self.bind[num].set("Key: {0} \n Instrument: {1} \n Tone: {2}".format(self.key[num], self.instrument[num], self.tone[num]))
		self.bindWindow.destroy()
		
	def bindCancel(self):
		self.bindWindow.destroy()
		
	# Plays back notes.
	def functionality(self, event):
		key_on = event.char
		
		if (key_on == "+" and self.octave + 84 < 127):
			self.octave += 12
			self.currentOctaveText.set("Current octave: {0}".format(int((self.octave/12)+4)))
		elif (key_on == "-" and self.octave - 84 > -127):
			self.octave -= 12
			self.currentOctaveText.set("Current octave: {0}".format(int((self.octave/12)+4)))
	
		if (key_on == "a"):
			self.outport.send(mido.Message('note_on', note=60+self.octave, velocity=64))		
		elif (key_on == "w"):
			self.outport.send(mido.Message('note_on', channel=1, note=61+self.octave, velocity=80))
		elif (key_on == "s"):
			self.outport.send(mido.Message('note_on', note=62+self.octave, velocity=80))
		elif (key_on == "e"):
			self.outport.send(mido.Message('note_on', note=63+self.octave, velocity=80))
		elif (key_on == "d"):
			self.outport.send(mido.Message('note_on', note=64+self.octave, velocity=80))
		elif (key_on == "f"):
			self.outport.send(mido.Message('note_on', note=65+self.octave, velocity=80))
		elif (key_on == "t"):
			self.outport.send(mido.Message('note_on', channel=1, note=66+self.octave, velocity=80))
		elif (key_on == "g"):
			self.outport.send(mido.Message('note_on', note=67+self.octave, velocity=80))
		elif (key_on == "y"):
			self.outport.send(mido.Message('note_on', note=68+self.octave, velocity=80))
		elif (key_on == "h"):
			self.outport.send(mido.Message('note_on', note=69+self.octave, velocity=80))
		elif (key_on == "u"):
			self.outport.send(mido.Message('note_on', note=70+self.octave, velocity=80))
		elif (key_on == "j"):
			self.outport.send(mido.Message('note_on', note=71+self.octave, velocity=80))
		elif (key_on == "k"):
			self.outport.send(mido.Message('note_on', note=72+self.octave, velocity=80))
				
		
root = Tk()
global config
config = configparser.ConfigParser()
prog = GUI(root)
root.mainloop()