import pygame
import math
import tkMessageBox
from ikLibraryBin import * # Inverse-Kinematic Library developed by Rob Cook, information on http://robcook.eu

# Core of this code taken and modified from example from: http://www.pygame.org/docs/ref/joystick.html

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printF(self, screen, textString):
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
    

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 200]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("PS3 SixAxis Hexy Controller")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# polling time between joystick event readings
pollIntervalSlow = 500 # slow poll time, time in ms
pollIntervalFast = 100 # fast poll time, time in ms
pollInterval = pollIntervalSlow

# loop start time
lastTime = pygame.time.get_ticks()

# record position in step sequence
stepID = 0

# variable to monitor rest status of Hexy
legsParked = 0

# -------- Main Program Loop -----------
# check that a PS3 controller has been connected
if pygame.joystick.get_count() == 0:
    # no joysticks attached
    # inform the user that they should connect a sixaxis controller
    tkMessageBox.showinfo("Error", "Please connect a joystick")

    pygame.quit () # and quit

if pygame.joystick.Joystick(0).get_name() != "Sony PLAYSTATION(R)3 Controller":
    # no sixaxis controller connected to pygame
    # inform the user that they should connect a sixaxis controller
    tkMessageBox.showinfo("Error", "Please connect a Sony PS3 Sixaxis controller")

    pygame.quit () # and quit

# keep looping until the user clicks quit
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    # check to see if the required time has passed before getting new joystick inputs        
    if pygame.time.get_ticks() - lastTime - 1 > pollInterval:
        lastTime = pygame.time.get_ticks() # record new time
        
        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # For each joystick:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printF(screen, "Joystick name: {}".format(name) )
        
        textPrint.printF(screen, "Joystick Processing")
        textPrint.indent()
        
        # read the joystick positions
        x = joystick.get_axis(0) # left stick left-right position
        y = joystick.get_axis(1) # left stick up-down position
        z = joystick.get_axis(2) # right stick left-right position
        
        # read the joystick button (L3)
        sprintFlag = joystick.get_button(1)
        textPrint.printF(screen, "L3 pressed? {}".format(sprintFlag))
        
        # calculate the angle the left stick is pointing in
        joyAngle = math.atan2(-x, -y)
        textPrint.printF(screen, "Direction of left-stick: {:>6.3f}".format(math.degrees(joyAngle)))
        
        # calculate the distance from centre
        # correction factor is because at 45 degrees the maximum magnitude is sqrt(2) = 1.414
        joyMagnitude = math.sqrt(x*x+y*y) * math.cos(math.pi/4-math.fabs(math.atan2(math.fabs(x), math.fabs(y))-math.pi/4))
        textPrint.printF(screen, "Magnitude of left-stick: {:>6.3f}".format(joyMagnitude))
        
        # if movement and rotation is required, with a total magnitude greater than unity
        if (joyMagnitude + math.fabs(z)) > 1:
            # scale both to a maximum of unity
            moveMag = joyMagnitude / (joyMagnitude + math.fabs(z))
            rotMag = z / (joyMagnitude + math.fabs(z))
        else:
            moveMag = joyMagnitude
            rotMag = z
            
        textPrint.printF(screen, "Corrected magnitude of movement input: {:>6.3f}".format(moveMag))
        textPrint.printF(screen, "Corrected magnitude of rotation input: {:>6.3f}".format(rotMag))

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # axis 12 and 13 for trigger buttons
        headDirection = joystick.get_axis(12) - joystick.get_axis(13)
        hexy.neck.set(80*headDirection)
        
        # perform leg movement
        s = 23 * moveMag
        if moveMag == 0 and rotMag == 0:
            # no input, remove sprint action
            pollInterval = pollIntervalSlow
            
            # no movement requested at all, park legs and start wait timer
            if legsParked:
                if pygame.time.get_ticks() - parkStartTime > 2000: # check if two seconds have passed since legs were parked
                    # if this is the first time here, send the kill command to all the servos
                    if legsParked != 2:
                        # kill all servos
                        hexy.con.killAll()
                    # set the flag to ignore the serial command on subsequent visits
                    legsParked = 2
                else:
                    # park all the legs on the ground in the neutral position
                    hexyTripod1GlobalOffset(0,0,0)
                    hexyTripod2GlobalOffset(0,0,0)
                    hexy.con.sendBinary()
            else:
                # put the start to park the legs
                if stepID == 0:
                    hexyTripod1GlobalOffset(0,0,-30)
                    hexyTripod2GlobalOffset(0,0,0)
                    hexy.con.sendBinary()
                else:
                    hexyTripod1GlobalOffset(0,0,0)
                    hexyTripod2GlobalOffset(0,0,-30)
                    hexy.con.sendBinary()
                # highlight that the leg parking procedure has started
                legsParked = 1
                # log the time
                parkStartTime = pygame.time.get_ticks()
            # stepID will be augmented at the end of the program loop, so this ensures that the next movement step starts at stepID == 0
            stepID = -1
        else:
            # check if sprintFlag has been set
            if sprintFlag:
                pollInterval = pollIntervalFast # speed things up, will only be slowed down when no input received
            
            # movement asked for
            legsParked = 0 # legs aren't parked
            if stepID == 0:
                # step position 0
                hexyTripod1GlobalOffset(0,0,-30)
                hexyTripod2GlobalOffset(0,0,0)
            elif stepID == 1:
                # step position 1
                hexyTripod1GlobalOffsetRot(math.sin(joyAngle)*s,-math.cos(joyAngle)*s,0, -0.15*rotMag)
                hexyTripod2GlobalOffsetRot(-math.sin(joyAngle)*s,math.cos(joyAngle)*s,0, 0.15*rotMag)
            elif stepID == 2:
                # step position 2
                hexyTripod1GlobalOffset(0,0,0)
                hexyTripod2GlobalOffset(0,0,-30)
            elif stepID == 3:
                # step position 3
                hexyTripod1GlobalOffsetRot(-math.sin(joyAngle)*s,math.cos(joyAngle)*s,0, 0.15*rotMag)
                hexyTripod2GlobalOffsetRot(math.sin(joyAngle)*s,-math.cos(joyAngle)*s,0, -0.15*rotMag)
            hexy.con.sendBinary()
            
        # increment the stepID
        stepID += 1
        if stepID == 4:
            stepID = 0 # loop back to zero, so that there are four step phases in a loop

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
# TODO seems to crash from PoMoCo if executed twice. Must identify why this is...
pygame.quit ()
