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
		
		# Initializes mido, the MIDI outport, and global variables that are used in functionality().
		midi_out = mido.get_output_names()
		self.octave = 0
		self.counter = -1
		
		# Sets up octave display. Every time it's changed via + or -, the display updates accordingly (via statements in functionality())
		self.currentOctaveText = StringVar()
		self.currentOctaveText.set("Current octave: %d" % ((self.octave/12)+4))
		octaveDisplay = Label(master, textvariable=self.currentOctaveText, anchor=NE)
		octaveDisplay.pack()
		
		# Any key that's pressed activates functionality(), which plays notes.
		master.bind("<Key>", self.functionality)
		
		# Combo box and apply button for selecting MIDI port.
		self.port = StringVar(master)
		self.port.set(midi_out[0])
		self.currentPort = self.port
		portSelect = OptionMenu(master, self.port, *midi_out)
		portSelect.pack(side=LEFT)
		applyPortButton = Button(master, text="Apply", command=self.applyPort)
		applyPortButton.pack(side=RIGHT)
		self.outport = mido.open_output(self.currentPort.get())
	
	# Uses an apply button to change output MIDI port.
	def applyPort(self):
		self.currentPort = self.port
		self.outport.close()
		self.outport = mido.open_output(self.currentPort.get())

	
	# buttonManager is the window that will allow users to bind keys for sound playback.
	def buttonManager(self):
		# Globals hell yeah
		global config
		
		# Config file setup; may or may not keep.
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
		buttonMgr = Toplevel(self.window)
		buttonMgr.grab_set()
		buttonMgr.focus_set()
		buttonMgr.maxsize()
		buttonMgr.title("Button Manager")
		
		# Sets up text labels for binding instructions and the notes/binds.
		instructions = Label(buttonMgr, text="Click a note and then press any key to bind that key to the given note.")
		instructions.pack()

				
	# Plays back notes.
	def functionality(self, event):
		key_on = event.char
		
		if (key_on == "+" and self.octave + 84 < 127):
			self.octave += 12
			self.currentOctaveText.set("Current octave: %d" % ((self.octave/12)+4))
		elif (key_on == "-" and self.octave - 84 > -127):
			self.octave -= 12
			self.currentOctaveText.set("Current octave: %d" % ((self.octave/12)+4))
	
		if (key_on == "a"):
			self.outport.send(mido.Message('note_on', note=60+self.octave, velocity=80))		
		elif (key_on == "w"):
			self.outport.send(mido.Message('note_on', note=61+self.octave, velocity=80))
		elif (key_on == "s"):
			self.outport.send(mido.Message('note_on', note=62+self.octave, velocity=80))
		elif (key_on == "e"):
			self.outport.send(mido.Message('note_on', note=63+self.octave, velocity=80))
		elif (key_on == "d"):
			self.outport.send(mido.Message('note_on', note=64+self.octave, velocity=80))
		elif (key_on == "f"):
			self.outport.send(mido.Message('note_on', note=65+self.octave, velocity=80))
		elif (key_on == "t"):
			self.outport.send(mido.Message('note_on', note=66+self.octave, velocity=80))
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

		self.counter += 1
		if (self.counter % 2 == 0):		
			o_up = False
			o_down = False
			reset = False
		if (self.counter == 100):
				self.counter = 0	
				

root = Tk()
global config
config = configparser.ConfigParser()
prog = GUI(root)
root.mainloop()