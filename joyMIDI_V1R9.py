import pygame
import mido
from mido import Message
import os
import numpy as np
import mido.backends.rtmidi
import configparser

config = configparser.ConfigParser()

# Config file setup/reading. Uses strings with commas separating list items to store in the file.
if (os.path.isfile('settings.ini')):
    config.read('settings.ini')
    keyString = config.get('Joy Binds','inputs')
    instrumentString = config.get('Joy Binds', 'instruments')
    toneString = config.get('Joy Binds', 'notes')
    
    inputs = keyString.split(",")
    instrument = instrumentString.split(",")
    notes = toneString.split(",")

    for i in range(16):
        if inputs[i] != " Empty" and inputs[i] != "Empty": 
            inputs[i] = int(inputs[i])
        if instrument[i] != " Empty" and instrument[i] != "Empty":
            instrument[i] = int(instrument[i])
        if notes[i] != " Empty" and notes[i] != "Empty": 
            notes[i] = int(notes[i])

else:
    key = ["Empty"]*16
    instrument = [0]*16
    stone = [0]*16
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
#This version is for use with python 3

#Mido gets the name of all the output ports
print(mido.get_output_names())

#User decides what port to use
userPort = input('Enter the port you would like to use: ')

outport = mido.open_output(userPort)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

#This is for a wider controller support
safeCheck1=0
safeCheck2=0


#This function is what determines when to play which note from which button
#button_was_pressed is equal to 0 when it has gone two frames without being pressed.
#It is equal to 1 when it has gone one frame without being pressed.
#And equal to two when it is pressed.
def signalOnPress(note1, button1):
    if button == 1 and i == button1 and button_was_pressed[i] ==0 and safeCheck1==1:
        outport.send(mido.Message('note_on', note=note1, velocity=100, channel=0))
        button_was_pressed[i] = 1
    elif button == 0 and i == button1 and button_was_pressed[i] ==1 and safeCheck2==1:
        outport.send(mido.Message('note_off', note=note1, velocity=100, channel=0))
        button_was_pressed[i] = 2
    elif button == 0 and i == button1 and button_was_pressed[i] ==2 and safeCheck2==1:
        button_was_pressed[i] = 0

#This is for printing to the pygame screen
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
  
#Starts pygame
pygame.init()
 
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
    
#This will be used for the dead zone on the controller sticks    
absolute_axis = 0

#This array holds the state of each button.
button_was_pressed = np.zeros(25)    

# Get ready to print
textPrint = TextPrint()

#This is used for pitch bend
pith=0

#These are used for debugging, making sure the code is reading the button inputs
Ding = "ding"
Dong = "dong"
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
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()
 
        #Here are the button mappings and the playing of the notes
        for i in range( buttons ):
            button = joystick.get_button( i )


            signalOnPress(60, 0) 
   
            signalOnPress(notes[1], inputs[1])

            signalOnPress(notes[2], inputs[2]) 

            signalOnPress(notes[3], inputs[3])    

            signalOnPress(notes[4], inputs[4])

            signalOnPress(notes[5], inputs[5])                                                                         

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
    clock.tick(240)

    #outport.reset()
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
