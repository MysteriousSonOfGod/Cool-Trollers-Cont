from tkinter import *
import configparser
import os.path
import mido
from mido import Message
import mido.backends.rtmidi
import fnmatch
import pygame
import numpy as np

class GUI:
	def __init__(self, master, config):
		# Sets up main window and global config.
		self.window = master
		self.config = config
		master.title("Cooltrollers")
		#master.iconbitmap(default="controller.ico")
		
		# Adds menus.
		menuBar = Menu(master)
		fileMenu = Menu(menuBar, tearoff=0)
		optionsMenu = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="File", menu=fileMenu)
		fileMenu.add_command(label="Controller", command=lambda:Controller(self.outport, self.config, self.instruString))
		fileMenu.add_command(label="Exit", command=sys.exit)
		menuBar.add_cascade(label="Options", menu=optionsMenu)
		optionsMenu.add_command(label="Button Manager", command=self.buttonManager)
		optionsMenu.add_command(label="Controller Manager", command=self.controllerManager)
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
		octaveDisplay.grid(row=0, columnspan=2)
		
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
		
		# Setting up proper binding settings for playback.
		# This right here is all the General MIDI instruments in one list.
		self.instruList = ['1 Acoustic Grand Piano', '2 Bright Acoustic Piano', '3 Electric Grand Piano','4 Honky-tonk Piano', '5 Electric Piano 1', '6 Electric Piano 2', '7 Harpsichord', '8 Clavinet', '9 Celesta', '10 Glockenspiel', '11 Music Box', '12 Vibraphone', '13 Marimba', '14 Xylophone', '15 Tubular Bells', '16 Dulcimer', '17 Drawbar Organ', '18 Percussive Organ', '19 Rock Organ', '20 Church Organ', '21 Reed Organ', '22 Accordion', '23 Harmonica', '24 Tango Accordion', '25 Acoustic Guitar (nylon)', '26 Acoustic Guitar (steel)', '27 Electric Guitar (jazz)', '28 Electric Guitar (clean)', '29 Electric Guitar (muted)', '30 Overdriven Guitar', '31 Distortion Guitar', '32 Guitar harmonics', '33 Acoustic Bass', '34 Electric Bass (finger)', '35 Electric Bass (pick)', '36 Fretless Bass', '37 Slap Bass 1', '38 SlapBass 2', '39 Synth Bass 1', '40 Synth Bass 2', '41 Violin', '42 Viola', '43 Cello', '44 Contrabass', '45 Tremolo Strings', '46 Pizzicato Strings', '47 Orchestral Harp', '48 Timpani', '49 String Ensemble 1', '50 String Ensemble 2', '51 Synth Strings 1', '52 Synth Strings 2', '53 Choir Aahs', '54 Voice Oohs', '55 Synth Voice', '56 Orchestra Hit', '57 Trumpet', '58 Trombone', '59 Tuba', '60 Muted Trumpet', '61 French Horn', '62 Brass Section', '63 Synth Brass 1', '64 Synth Brass 2', '65 Soprano Sax', '66 Alto Sax', '67 Tenor Sax', '68 Baritone Sax', '69 Oboe', '70 English Horn', '71 Bassoon', '72 Clarinet', '73 Piccolo', '74 Flute', '75 Recorder', '76 Pan Flute', '77 Blown Bottle', '78 Shakuhachi', '79 Whistle', '80 Ocarina', '81 Lead 1 (square)', '82 Lead 2 (sawtooth)', '83 Lead 3 (calliope)', '84 Lead 4 (chiff)', '85 Lead 5 (charang)', '86 Lead 6 (voice)', '87 Lead 7 (fifths)', '88 Lead 8 (bass + lead)', '89 Pad 1 (new age)', '90 Pad 2 (warm)', '91 Pad 3 (polysynth)', '92 Pad 4 (choir)', '93 Pad 5 (bowed)', '94 Pad 6 (metallic)', '95 Pad 7 (halo)', '96 Pad 8 (sweep)', '97 FX 1 (rain)', '98 FX 2 (soundtrack)', '99 FX 3 (crystal)', '100 FX 4 (atmosphere)', '101 FX 5 (brightness)', '102 FX 6 (goblins)', '103 FX 7 (echoes)', '104 FX 8 (sci-fi)', '105 Sitar', '106 Banjo', '107 Shamisen', '108 Koto', '109 Kalimba', '110 Bag pipe', '111 Fiddle','112 Shanai', '113 Tinkle Bell', '114 Agogo', '115 Steel Drums', '116 Woodblock', '117 Taiko Drum', '118 Melodic Tom', '119 Synth Drum', '120 Reverse Cymbal', '121 Guitar Fret Noise', '122 Breath Noise', '123 Seashore', '124 Bird Tweet', '125 Telephone Ring', '126 Helicopter', '127 Applause', '128 Gunshot']
		
		# Checks whether there's a settings file. Otherwise, the user must set up button binds in the bind manager.
		if (os.path.isfile('settings.ini')):
			self.config.read('settings.ini')
			keyString = self.config.get('Button Binds', 'Keys')
			instrumentString = self.config.get('Button Binds', 'Instruments')
			noteString = self.config.get('Button Binds', 'Notes')
			self.key = keyString.split(",")
			self.instruString = instrumentString.split(",")
			self.note = noteString.split(",")
			
			buttonString = self.config.get('Joystick Binds', 'Buttons')
			btnInstrumentString = self.config.get('Joystick Binds', 'Instruments')
			btnNoteString = self.config.get('Joystick Binds', 'Notes')
			self.button = buttonString.split(",")
			self.btnInstruString = btnInstrumentString.split(",")
			self.btnNote = btnNoteString.split(",")
			
			for x in range(16):
				self.button[x] = int(self.button[x])
			
		else:
			# Config file initial setup. Uses strings with commas separating list items to store in the file.
			self.clearBinds()
			self.clearCtrlBinds()
		
		# Getting the number of the instrument for passing to mido.
		for x in range(16):
			if (self.instruString[x][1] == ' '):
				self.instruNum = int(self.instruString[x][0])
			elif (self.instruString[x][2] == ' '):
				self.instruNum = int(self.instruString[x][:2])
			else:
				self.instruNum = int(self.instruString[x][:3])
			
			self.outport.send(mido.Message('program_change', channel=x, program=self.instruNum-1))
		
	# Uses an apply button to change output MIDI port.
	def applyPort(self):
		self.currentPort = self.port
		self.outport.close()
		self.outport = mido.open_output(self.currentPort.get())
		
		for x in range(16):
			if (self.instruString[x][1] == ' '):
				self.instruNum = int(self.instruString[x][0])
			elif (self.instruString[x][2] == ' '):
				self.instruNum = int(self.instruString[x][:2])
			else:
				self.instruNum = int(self.instruString[x][:3])
			self.outport.send(mido.Message('program_change', channel=x, program=self.instruNum-1))
			
	# buttonManager is the window that will allow users to bind keys for sound playback.
	def buttonManager(self):
		# Window setup.
		self.buttonMgr = Toplevel(self.window)
		self.buttonMgr.grab_set()
		self.buttonMgr.focus_set()
		self.buttonMgr.title("Button Manager")
		self.buttonMgr.resizable(0,0)
		
		# Sets up text label for binding instructions.
		instructions = Label(self.buttonMgr, text="Click a button to access binding settings.")
		instructions.grid(columnspan=3)
		
		# Clear All button for removing all binds.
		clear = Button(self.buttonMgr, text="Clear All", command=self.clearBinds)
		clear.grid(column=3)
		
		# Sets up sixteen buttons for binding keys.
		r = 0
		c = 0
		button=[None]*16
		self.bind = [None]*16
		
		for x in range(16):
			self.bind[x] = StringVar()
			self.bind[x].set("Key: {0} \n Instrument: {1} \n note: {2}".format(self.key[x], self.instruString[x], self.note[x]))
		self.bind[9].set("PERCUSSION")
			
		# This is gross but bear with me
		button[0] = Button(self.buttonMgr, textvariable=self.bind[0], command=lambda: self.binding(self.key[0], self.instruString[0], self.note[0], 0))
		button[1] = Button(self.buttonMgr, textvariable=self.bind[1], command=lambda: self.binding(self.key[1], self.instruString[1], self.note[1], 1))
		button[2] = Button(self.buttonMgr, textvariable=self.bind[2], command=lambda: self.binding(self.key[2], self.instruString[2], self.note[2], 2))
		button[3] = Button(self.buttonMgr, textvariable=self.bind[3], command=lambda: self.binding(self.key[3], self.instruString[3], self.note[3], 3))
		button[4] = Button(self.buttonMgr, textvariable=self.bind[4], command=lambda: self.binding(self.key[4], self.instruString[4], self.note[4], 4))
		button[5] = Button(self.buttonMgr, textvariable=self.bind[5], command=lambda: self.binding(self.key[5], self.instruString[5], self.note[5], 5))
		button[6] = Button(self.buttonMgr, textvariable=self.bind[6], command=lambda: self.binding(self.key[6], self.instruString[6], self.note[6], 6))
		button[7] = Button(self.buttonMgr, textvariable=self.bind[7], command=lambda: self.binding(self.key[7], self.instruString[7], self.note[7], 7))
		button[8] = Button(self.buttonMgr, textvariable=self.bind[8], command=lambda: self.binding(self.key[8], self.instruString[8], self.note[8], 8))
		button[9] = Button(self.buttonMgr, textvariable=self.bind[9], command=lambda: self.binding(self.key[9], self.instruString[9], self.note[9], 9))
		button[9].config(state="disabled", height=3)
		button[10] = Button(self.buttonMgr, textvariable=self.bind[10], command=lambda: self.binding(self.key[10], self.instruString[10], self.note[10], 10))
		button[11] = Button(self.buttonMgr, textvariable=self.bind[11], command=lambda: self.binding(self.key[11], self.instruString[11], self.note[11], 11))
		button[12] = Button(self.buttonMgr, textvariable=self.bind[12], command=lambda: self.binding(self.key[12], self.instruString[12], self.note[12], 12))
		button[13] = Button(self.buttonMgr, textvariable=self.bind[13], command=lambda: self.binding(self.key[13], self.instruString[13], self.note[13], 13))
		button[14] = Button(self.buttonMgr, textvariable=self.bind[14], command=lambda: self.binding(self.key[14], self.instruString[14], self.note[14], 14))
		button[15] = Button(self.buttonMgr, textvariable=self.bind[15], command=lambda: self.binding(self.key[15], self.instruString[15], self.note[15], 15))
		
		r = 1
		for x in range(16):
			c += 1
			if (x % 4 == 0):
				r += 1
				c = 0
			button[x].grid(row=r, column=c)
			button[x].config(width=30)
			
	# Window that opens for every bind clicked for configuration.
	def binding(self, key, instr, note, num):
		self.bindWindow = Toplevel(self.buttonMgr)
		self.bindWindow.title("Bind Configuration")
		self.bindWindow.focus_set()
		
		# Key binding.
		keyLabel = Label(self.bindWindow, text="Key: ")
		keyLabel.grid(row=0, column=0)
		self.keyBindDisplay = StringVar()
		self.keyBindDisplay.set(key)
		self.newKey = key
		keyBind = Button(self.bindWindow, textvariable=self.keyBindDisplay, command=self.press_key)
		keyBind.grid(row=0, column=1)
		
		# Instrument binding.
		instrLabel = Label(self.bindWindow, text="Instrument: ")
		instrLabel.grid(row=1)
		self.instrument = StringVar()
		self.instrument.set(instr)
		instruBind = OptionMenu(self.bindWindow, self.instrument, *self.instruList)
		instruBind.grid(row=1, column=1)
		
		# Note binding.
		noteLabel = Label(self.bindWindow, text="Note: ")
		noteLabel.grid(row=2)
		self.noteLetter = StringVar()
		self.noteLetter.set(note)
		noteList = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		noteBind = OptionMenu(self.bindWindow, self.noteLetter, *noteList)
		noteBind.grid(row=2, column=1)
		
		# OK and Cancel buttons.
		buttonOK = Button(self.bindWindow, text="OK", command=lambda:self.bindOK(num))
		buttonCancel = Button(self.bindWindow, text="Cancel", command=self.bindWindow.destroy)
		buttonOK.grid(row=3,column=1)
		buttonCancel.grid(row=3, column=0)
	
	# The next two functions are exclusively for key-binding special stuff.
	def press_key(self):
		self.keyBindDisplay.set("Press any key...")
		self.bindWindow.bind("<Key>", self.key_bound)
		
	def key_bound(self, event):
		self.newKey = event.char
		self.keyBindDisplay.set(self.newKey)
		self.bindWindow.unbind("<Key>")
	
	# Saves changes when the OK button is pressed.
	def bindOK(self, num):
		self.key[num] = self.newKey
		self.instruString[num] = self.instrument.get()
		self.note[num] = self.noteLetter.get()
		self.bind[num].set("Key: {0} \n Instrument: {1} \n Note: {2}".format(self.newKey, self.instrument.get(), self.noteLetter.get()))
		
		instruNum = ""
		if (self.instrument.get()[1] == ' '):
			instruNum = int(self.instrument.get()[0])
		elif (self.instrument.get()[2] == ' '):
			instruNum = int(self.instrument.get()[:2])
		else:
			instruNum = int(self.instrument.get()[:3])
		
		self.outport.send(mido.Message('program_change', channel=num, program=instruNum-1))
		
		keyString = ""
		instrumentString = ""
		noteString = ""
		
		for x in range(16):
			keyString += (self.key[x] + ",") 
			instrumentString += (self.instruString[x] + ",")
			noteString += (self.note[x] + ",") 
			self.config['Button Binds'] = {'Keys':keyString, 'Instruments':instrumentString, 'Notes':noteString}
		with open('settings.ini', 'w') as configfile:
			self.config.write(configfile)
			
		self.bindWindow.destroy()
	
	# Button bindings for a controller.
	def controllerManager(self):
		pygame.init()
		pygame.joystick.init()
		for i in range(pygame.joystick.get_count()):
			self.joystick = pygame.joystick.Joystick(i)
			self.joystick.init()
		# Window setup.
		self.ctrlMgr = Toplevel(self.window)
		self.ctrlMgr.grab_set()
		self.ctrlMgr.focus_set()
		self.ctrlMgr.title("Controller Manager")
		self.ctrlMgr.resizable(0,0)
		
		# Sets up text label for binding instructions.
		instructions = Label(self.ctrlMgr, text="Click a button to access binding settings.")
		instructions.grid(columnspan=3)
		
		# Clear All button for removing all binds.
		clear = Button(self.ctrlMgr, text="Clear All", command=self.clearCtrlBinds)
		clear.grid(column=3)
		
		# Sets up sixteen buttons for binding keys.
		r = 0
		c = 0
		button=[None]*16
		self.ctrlbind = [None]*16
		
		for x in range(16):
			self.ctrlbind[x] = StringVar()
			self.ctrlbind[x].set("Button: {0} \n Instrument: {1} \n Note: {2}".format(self.button[x], self.btnInstruString[x], self.btnNote[x]))
		self.ctrlbind[9].set("PERCUSSION")
			
		# This is gross but bear with me
		button[0] = Button(self.ctrlMgr, textvariable=self.ctrlbind[0], command=lambda: self.ctrlbinding(self.button[0], self.btnInstruString[0], self.btnNote[0], 0))
		button[1] = Button(self.ctrlMgr, textvariable=self.ctrlbind[1], command=lambda: self.ctrlbinding(self.button[1], self.btnInstruString[1], self.btnNote[1], 1))
		button[2] = Button(self.ctrlMgr, textvariable=self.ctrlbind[2], command=lambda: self.ctrlbinding(self.button[2], self.btnInstruString[2], self.btnNote[2], 2))
		button[3] = Button(self.ctrlMgr, textvariable=self.ctrlbind[3], command=lambda: self.ctrlbinding(self.button[3], self.btnInstruString[3], self.btnNote[3], 3))
		button[4] = Button(self.ctrlMgr, textvariable=self.ctrlbind[4], command=lambda: self.ctrlbinding(self.button[4], self.btnInstruString[4], self.btnNote[4], 4))
		button[5] = Button(self.ctrlMgr, textvariable=self.ctrlbind[5], command=lambda: self.ctrlbinding(self.button[5], self.btnInstruString[5], self.btnNote[5], 5))
		button[6] = Button(self.ctrlMgr, textvariable=self.ctrlbind[6], command=lambda: self.ctrlbinding(self.button[6], self.btnInstruString[6], self.btnNote[6], 6))
		button[7] = Button(self.ctrlMgr, textvariable=self.ctrlbind[7], command=lambda: self.ctrlbinding(self.button[7], self.btnInstruString[7], self.btnNote[7], 7))
		button[8] = Button(self.ctrlMgr, textvariable=self.ctrlbind[8], command=lambda: self.ctrlbinding(self.button[8], self.btnInstruString[8], self.btnNote[8], 8))
		button[9] = Button(self.ctrlMgr, textvariable=self.ctrlbind[9], command=lambda: self.ctrlbinding(self.button[9], self.btnInstruString[9], self.btnNote[9], 9))
		button[9].config(state="disabled", height=3)
		button[10] = Button(self.ctrlMgr, textvariable=self.ctrlbind[10], command=lambda: self.ctrlbinding(self.button[10], self.btnInstruString[10], self.btnNote[10], 10))
		button[11] = Button(self.ctrlMgr, textvariable=self.ctrlbind[11], command=lambda: self.ctrlbinding(self.button[11], self.btnInstruString[11], self.btnNote[11], 11))
		button[12] = Button(self.ctrlMgr, textvariable=self.ctrlbind[12], command=lambda: self.ctrlbinding(self.button[12], self.btnInstruString[12], self.btnNote[12], 12))
		button[13] = Button(self.ctrlMgr, textvariable=self.ctrlbind[13], command=lambda: self.ctrlbinding(self.button[13], self.btnInstruString[13], self.btnNote[13], 13))
		button[14] = Button(self.ctrlMgr, textvariable=self.ctrlbind[14], command=lambda: self.ctrlbinding(self.button[14], self.btnInstruString[14], self.btnNote[14], 14))
		button[15] = Button(self.ctrlMgr, textvariable=self.ctrlbind[15], command=lambda: self.ctrlbinding(self.button[15], self.btnInstruString[15], self.btnNote[15], 15))
		
		r = 1
		for x in range(16):
			c += 1
			if (x % 4 == 0):
				r += 1
				c = 0
			button[x].grid(row=r, column=c)
			button[x].config(width=30)
	
	def ctrlbinding(self, btn, instr, note, num):
		self.bindWindow = Toplevel(self.ctrlMgr)
		self.bindWindow.title("Bind Configuration")
		self.bindWindow.focus_set()
		
		# Key binding.
		btnLabel = Label(self.bindWindow, text="Button: ")
		btnLabel.grid(row=0, column=0)
		self.bindDisplay = StringVar()
		self.bindDisplay.set(btn)
		self.newBtn = btn
		btnBind = Button(self.bindWindow, textvariable=self.bindDisplay, command=lambda:self.press_btn(num))
		btnBind.grid(row=0, column=1)
		
		# Instrument binding.
		instrLabel = Label(self.bindWindow, text="Instrument: ")
		instrLabel.grid(row=1)
		self.ctrlInstrument = StringVar()
		self.ctrlInstrument.set(instr)
		instruBind = OptionMenu(self.bindWindow, self.ctrlInstrument, *self.instruList)
		instruBind.grid(row=1, column=1)
		
		# Note binding.
		noteLabel = Label(self.bindWindow, text="Note: ")
		noteLabel.grid(row=2)
		self.noteLetter = StringVar()
		self.noteLetter.set(note)
		noteList = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
		noteBind = OptionMenu(self.bindWindow, self.noteLetter, *noteList)
		noteBind.grid(row=2, column=1)
		
		# OK and Cancel buttons.
		buttonOK = Button(self.bindWindow, text="OK", command=lambda:self.ctrlBindOK(num))
		buttonCancel = Button(self.bindWindow, text="Cancel", command=self.bindWindow.destroy)
		buttonOK.grid(row=3,column=1)
		buttonCancel.grid(row=3, column=0)
		
	def press_btn(self, num):
		self.bindDisplay.set("Press any button...")
		buttons = self.joystick.get_numbuttons()
		done = False
		while not done:
			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN:
					for i in range(buttons):
						if self.joystick.get_button(i) == 1:
							self.button[num] = i
					done = True
		self.bindDisplay.set(str(self.button[num]))
					
	def ctrlBindOK(self, num):
		self.btnInstruString[num] = self.ctrlInstrument.get()
		self.btnNote[num] = self.noteLetter.get()
		self.ctrlbind[num].set("Key: {0} \n Instrument: {1} \n Note: {2}".format(str(self.button[num]), self.ctrlInstrument.get(), self.noteLetter.get()))
		
		instruNum = ""
		if (self.ctrlInstrument.get()[1] == ' '):
			instruNum = int(self.ctrlInstrument.get()[0])
		elif (self.ctrlInstrument.get()[2] == ' '):
			instruNum = int(self.ctrlInstrument.get()[:2])
		else:
			instruNum = int(self.ctrlInstrument.get()[:3])
		
		self.outport.send(mido.Message('program_change', channel=num, program=instruNum-1))
		
		buttonString = ""
		buttonInstrumentString = ""
		buttonNoteString = ""
		
		for x in range(16):
			buttonString += (str(self.button[x]) + ",") 
			buttonInstrumentString += (self.btnInstruString[x] + ",")
			buttonNoteString += (self.btnNote[x] + ",") 
			self.config['Joystick Binds'] = {'Buttons':buttonString, 'Instruments':buttonInstrumentString, 'Notes':buttonNoteString}
		with open('settings.ini', 'w') as configfile:
			self.config.write(configfile)
			
		self.bindWindow.destroy()
	
	# Clearing all binds, or creating a blank settings file.
	def clearBinds(self):
		self.key = ["Empty"]*16
		self.instruString = ["1 Acoustic Grand Piano"]*16
		self.note = ["C"]*16
		
		keyString = ""
		instrumentString = ""
		noteString = ""
		for x in range(16):
			keyString += (self.key[x] + ",") 
			instrumentString += (self.instruString[x] + ",") 
			noteString += (self.note[x] + ",")

		self.config['Button Binds'] = {'Keys':keyString, 'Instruments':instrumentString, 'Notes':noteString}
		with open('settings.ini', 'w') as configfile:
			self.config.write(configfile)
		
		# This is to make sure the bind button labels aren't set when they don't exist.
		# This function also runs when the settings file doesn't exist, so that'd be the case when this would do nothing.
		try:
			self.bind
		except:
			pass
		else:
			for x in range(16):
				if x!=9:
					self.bind[x].set("Key: {0} \n Instrument: {1} \n Note: {2}".format(self.key[x], self.instruString[x], self.note[x]))
				
	def clearCtrlBinds(self):
		self.button = [0]*16
		self.btnInstruString = ["1 Acoustic Grand Piano"]*16
		self.btnNote = ["C"]*16
		
		buttonString = ""
		btnInstrumentString = ""
		btnNoteString = ""
			
		for x in range(16):
			buttonString += (str(self.button[x]) + ",")
			instrumentString += (self.instruString[x] + ",") 
			noteString += (self.note[x] + ",")
			
		self.config['Joystick Binds'] = {'Buttons':buttonString, 'Instruments':instrumentString, 'Notes':noteString}
		with open('settings.ini', 'w') as configfile:
			self.config.write(configfile)
		
		# This is to make sure the bind button labels aren't set when they don't exist.
		# This function also runs when the settings file doesn't exist, so that'd be the case when this would do nothing.
		try:
			self.ctrlbind
		except:
			pass
		else:
			for x in range(16):
				if x!=9:
					self.ctrlbind[x].set("Button: {0} \n Instrument: {1} \n Note: {2}".format(self.button[x], self.btnInstruString[x], self.btnNote[x]))
			
	# Converts note letters to mido language.
	def noteToValue(self, letter):
		if letter == 'C':
			note_value = 60
		elif letter == 'C#':
			note_value = 61
		elif letter == 'D':
			note_value = 62
		elif letter == 'D#':
			note_value = 63
		elif letter == 'E':
			note_value = 64
		elif letter == 'F':
			note_value = 65
		elif letter == 'F#':
			note_value = 66
		elif letter == 'G':
			note_value = 67
		elif letter == 'G#':
			note_value = 68
		elif letter == 'A':
			note_value = 69
		elif letter == 'A#':
			note_value = 70
		elif letter == 'B':
			note_value = 71
		return note_value
			
	# Converts mido language to note letters.
	def valueToNote(self, note_value):
		if note_value == 60:
			letter = 'C'
		elif note_value == 61:
			letter = 'C#'
		elif note_value == 62:
			letter = 'D'
		elif note_value == 63:
			letter = 'D#'
		elif note_value == 64:
			letter = 'E'
		elif note_value == 65:
			letter = 'F'
		elif note_value == 66:
			letter = 'F#'
		elif note_value == 67:
			letter = 'G'
		elif note_value == 68:
			letter = 'G#'
		elif note_value == 69:
			letter = 'A'
		elif note_value == 70:
			letter = 'A#'
		elif note_value == 71:
			letter = 'B'
		return letter
			
	# Plays back notes.
	def functionality(self, event):
		key_on = event.char
		# Increasing or decreasing octave.
		if (key_on == "+" and self.octave + 84 < 127):
			self.octave += 12
			self.currentOctaveText.set("Current octave: {0}".format(int((self.octave/12)+4)))
		elif (key_on == "-" and self.octave - 84 > -127):
			self.octave -= 12
			self.currentOctaveText.set("Current octave: {0}".format(int((self.octave/12)+4)))
		
		# Actual playback.
		if (key_on in self.key):
			num = self.key.index(key_on)
			self.outport.send(mido.Message('note_on', channel=num, note=self.noteToValue(self.note[num])+self.octave, velocity=60))
			
# This is for printing to the pygame screen
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printTo(self, screen, textString):
        textBitmap = self.font.render(textString, True, self.BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

class Controller:
	def __init__(self, outport, config, kbInstr):
		self.outport = outport
		self.config = config
		self.kbInstrument = kbInstr
		
		# Define some colors
		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)

		# This is for a wider controller support
		self.safeCheck1=0
		self.safeCheck2=0
		
		# Starts pygame
		pygame.init()

		# Set the width and height of the screen [width,height]
		size = [500, 700]
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("joyMIDI")

		# Loop until the user clicks the close button.
		self.done = False

		# Used to manage how fast the screen updates
		clock = pygame.time.Clock()
		clock.tick(240)

		# Initialize the joysticks
		pygame.joystick.init()
    
		# This will be used for the dead zone on the controller sticks
		self.absolute_axis = 0

		# This array holds the state of each button.
		self.button_was_pressed = np.zeros(25)

		# This is used for pitch bend
		self.pith=0
		self.font = pygame.font.Font(None, 20)
		
		# Reading in controller settings.
		if (os.path.isfile('settings.ini')):
			buttonString = self.config.get('Joystick Binds', 'Buttons')
			instrumentString = self.config.get('Joystick Binds', 'Instruments')
			noteString = self.config.get('Joystick Binds', 'Notes')
			self.button = buttonString.split(",")
			self.instrument = instrumentString.split(",")
			self.note = noteString.split(",")
			
			instruNum=0
			for x in range(16):
				self.button[x] = int(self.button[x])
				if (self.instrument[x][1] == ' '):
					self.instrument[x] = int(self.instrument[x][0])
				elif (self.instrument[x][2] == ' '):
					self.instrument[x] = int(self.instrument[x][:2])
				else:
					self.instrument[x] = int(self.instrument[x][:3])
				self.outport.send(mido.Message('program_change', channel=x, program=self.instrument[x]-1))
				self.note[x] = GUI.noteToValue(self, self.note[x])
			
		self.main()
		
	# This function is what determines when to play which note from which button.
	# button_was_pressed equals 0 when it's gone two frames without being pressed, 1 when it's gone one frame without being pressed, and 2 when it is pressed.
	def signalOnPress(self, buttonOn, i):
		if buttonOn==1 and i in self.button and self.button_was_pressed[i]==0 and self.safeCheck1==1:
			num = self.button.index(i)
			self.outport.send(mido.Message('note_on', note=self.note[num], velocity=64, channel=num))
			self.button_was_pressed[i] = 1
		elif buttonOn==0 and i in self.button and self.button_was_pressed[i]==1 and self.safeCheck2==1:
			num = self.button.index(i)
			self.outport.send(mido.Message('note_off', note=self.note[num], velocity=64, channel=num))
			self.button_was_pressed[i] = 2
		elif buttonOn==0 and i in self.button and self.button_was_pressed[i]==2 and self.safeCheck2==1:
			self.button_was_pressed[i] = 0
		
	# -------- Main Program Loop -----------
	def main(self):
		while not self.done:
			# EVENT PROCESSING STEP
			for event in pygame.event.get(): # User did something
				if event.type == pygame.QUIT: # If user clicked close
					self.done=True # Flag that we are done so we exit this loop
        
				# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION

				# Here's the debugging events
				if event.type == pygame.JOYBUTTONDOWN:
					print("ding")
					self.safeCheck1=1
					self.safeCheck2=0
				if event.type == pygame.JOYBUTTONUP:
					print("dong")
					self.safeCheck1=0
					self.safeCheck2=1
            
			# DRAWING STEP
			# First, clear the screen to white. Don't put other drawing commands
			# above this, or they will be erased with this command.
			self.screen.fill(self.WHITE)
			TextPrint.reset(self)

			# Get count of joysticks
			joystick_count = pygame.joystick.get_count()
	
			TextPrint.printTo(self, self.screen, "Number of joysticks: {0}".format(joystick_count))
			TextPrint.indent(self)
    
			# For each joystick:
			for i in range(joystick_count):
				joystick = pygame.joystick.Joystick(i)
				joystick.init()
    
				TextPrint.printTo(self, self.screen, "Joystick {0}".format(i))
				TextPrint.indent(self)
    
				# Get the name from the OS for the controller/joystick.
				name = joystick.get_name()
				TextPrint.printTo(self, self.screen, "Joystick name: {0}".format(name))
        
				# Usually axis run in pairs, up/down for one, and left/right for the other.
				axes = joystick.get_numaxes()
				TextPrint.printTo(self, self.screen, "Number of axes: {0}".format(axes))
				TextPrint.indent(self)
				
				# Pitch bend.
				for i in range(axes):
					axis = joystick.get_axis(i)
					if axis < 0:
						self.absolute_axis = axis*-1
					else:
						self.absolute_axis = axis

					if i == 1 and (self.absolute_axis*8000 > 250):
						self.pith = -8000*axis
						for x in range(16):
							self.outport.send(mido.Message('pitchwheel', pitch = int(self.pith), channel=x))
           
				buttons = joystick.get_numbuttons()
				TextPrint.printTo(self, self.screen, "Number of buttons: {0}".format(buttons))
				TextPrint.indent(self)
 
				# Here are the button mappings and the playing of the notes.
				for i in range(buttons):
					self.signalOnPress(joystick.get_button(i), i)

				# Hat switch. All or nothing for direction, not like joysticks.
				# Value comes back in an array.
				hats = joystick.get_numhats()
				TextPrint.printTo(self, self.screen, "Number of hats: {0}".format(hats))
				TextPrint.indent(self)

				for i in range(hats):
					hat = joystick.get_hat(i)
					TextPrint.printTo(self, self.screen, "Hat {0} value: {1}".format(i, str(hat)))
				TextPrint.unindent(self)
				TextPrint.unindent(self)

    
			# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
			# Go ahead and update the screen with what we've drawn.
			pygame.display.flip()

		# Close the window and quit.
		# If you forget this line, the program will 'hang' on exit if running from IDLE.
		for x in range(16):
			if (self.kbInstrument[x][1] == ' '):
				instruNum = int(self.kbInstrument[x][0])
			elif (self.kbInstrument[x][2] == ' '):
				instruNum = int(self.kbInstrument[x][:2])
			else:
				instruNum = int(self.kbInstrument[x][:3])
			self.outport.send(mido.Message('program_change', channel=x, program=instruNum-1))
		pygame.quit()
	
root = Tk()
config = configparser.ConfigParser()
prog = GUI(root, config)
root.mainloop()