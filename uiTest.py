from tkinter import *
import tkinter as ttk
import pygame
import mido
from mido import Message
import os
import numpy as np
import mido.backends.rtmidi


 
note_convert = 0

print(mido.get_output_names())

userPort = input('Enter the port you would like to use: ')

outport = mido.open_output(userPort)

button_last_pressed = 0

button_config_array = np.zeros(25) 

pygame.init()

clock = pygame.time.Clock()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)


safeCheck1=0
safeCheck2=0

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
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

def noteToValue(Letter, note_value):
	if letter == 'C':
		note_value = 60
	if letter == 'C#':
		note_value = 61
	if letter == 'D':
		note_value = 62
	if letter == 'D#':
		note_value = 63
	if letter == 'E':
		note_value = 64
	if letter == 'F':
		note_value = 65
	if letter == 'F#':
		note_value = 66
	if letter == 'G':
		note_value = 67
	if letter == 'G#':
		note_value = 68
	if letter == 'A':
		note_value = 69
	if letter == 'A#':
		note_value = 70
	if letter == 'B':
		note_value = 71
														

def signalOnPress(note1, button1):
    if button == 1 and i == button1 and button_was_pressed[i] ==0 and safeCheck1==1:
        outport.send(mido.Message('note_on', note=note1, velocity=100, channel=0))
        button_was_pressed[i] = 1
    elif button == 0 and i == button1 and button_was_pressed[i] ==1 and safeCheck2==1:
        outport.send(mido.Message('note_off', note=note1, velocity=100, channel=0))
        button_was_pressed[i] = 2
    elif button == 0 and i == button1 and button_was_pressed[i] ==2 and safeCheck2==1:
        button_was_pressed[i] = 0 


root = Tk()
root.title("Config")


# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
 
# Create a Tkinter variable
tkvar = StringVar(root)
 
# Dictionary with options
choices_notes = { 'C','C#','D','D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#'}
tkvar.set('C') # set the default option
 
popupMenu = OptionMenu(mainframe, tkvar, *choices_notes)
Label(mainframe, text="Choose a note").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)
 
# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)


	
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

buttons = joystick.get_numbuttons()

for i in range( buttons ):
    button = joystick.get_button( i )
    if button == 1:
    	button_last_pressed = i
    	noteToValue(tkvar.get(), note_convert)
    	print(note_convert)
    	button_config_array[button_last_pressed] = note_convert 

    	
clock.tick(60)
root.mainloop()


# Used to manage how fast the screen updates

 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("joyMIDI")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
absolute_axis = 0

button_was_pressed = np.zeros(25)    
# Get ready to print
textPrint = TextPrint()
pith=0

Ding = "ding"
Dong = "dong"
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
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
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
         
   
        for i in range( axes ):
            '''
            axis = joystick.get_axis( i )
            if axis < 0:
                absolute_axis = axis*-1
            else:
                absolute_axis = axis

            if i == 1 and (absolute_axis*8000 > 250):
                pith = -8000*axis
                outport.send(mido.Message('pitchwheel', pitch = int(pith)))
'''            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()
 
        #button_was_pressed is equal to 0 when it has gone two frames without being pressed.
        #It is equal to 1 when it has gone one frame without being pressed.
        #And equal to two when it is pressed.
        for i in range( buttons ):
            button = joystick.get_button( i )

            print(note_convert)
            signalOnPress(note_convert, button_config_array[button])  
                                                                          

            #if button == 1 and i==1:
                #outport.send(mido.Message('control_change', value=100))    

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(120)

    #outport.reset()
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
