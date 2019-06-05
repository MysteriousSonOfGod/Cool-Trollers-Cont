import pygame
import mido
from mido import Message
import os
import mido.backends.rtmidi

#This version is for use with python 2


button_was_pressed = False
print(mido.get_output_names())
outport = mido.open_output("lport 3")

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
'''
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
'''    

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
#textPrint = TextPrint()
pith=500

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
        if event.type == pygame.JOYBUTTONUP:
            print(Dong)
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    #textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    #textPrint.print(screen, Number of joysticks: {}.format(joystick_count) )
    #textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        #textPrint.print(screen, Joystick {}.format(i) )
        #textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        #textPrint.print(screen, Joystick name: {}.format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        #textPrint.print(screen, Number of axes: {}.format(axes) )
        #textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            if i == 3:
                pith=500*axis
            
        buttons = joystick.get_numbuttons()
        #textPrint.print(screen, Number of buttons: {}.format(buttons) )
        #textPrint.indent()
 
        for i in range( buttons ):
            button = joystick.get_button( i )
            if button == 1 and i==0 and button_was_pressed == False:
                outport.send(mido.Message('note_on', note=62, velocity=80, channel=0))
                button_was_pressed = True                 
            elif button == 0 and i==0: 
                  button_was_pressed = False
            if button == 1 and i==1:
                outport.send(mido.Message('note_on', note=60, velocity=80, channel=0))
            #if button == 1 and i==1:
                #outport.send(mido.Message('note_on', note=60, velocity=80, channel=0)) 
                #outport.send(mido.Message('pitchwheel', pitch=-8000))               
            if button == 1 and i==2:
                outport.send(mido.Message('note_on', note=64, velocity=80, channel=0))        
            if button == 1 and i==3:
                outport.send(mido.Message('note_on', note=67, velocity=80, channel=0))
            if button == 1 and i==4:
                outport.send(mido.Message('note_on', note=69, velocity=80, channel=0)) 
            if button == 1 and i==5:
                outport.send(mido.Message('note_on', note=59, velocity=80, channel=0))   

            #if button == 1 and i==1:
                #outport.send(mido.Message('control_change', value=100))    

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        #textPrint.print(screen, Number of hats: {}.format(hats) )
        #textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            #textPrint.print(screen, Hat {} value: {}.format(i, str(hat)) )
        #textPrint.unindent()
        
        #textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(60)

    #outport.reset()
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
