# get console input from user
from Tkinter import *
import tkSimpleDialog
import time
from itertools import repeat
import math
from fontLib import letterPath
from ikLibrary import * # Inverse-Kinematic Library developed by Rob Cook, information on http://robcook.eu
   
def moveLetterWidthRight(s):
    # direction (CCW from forwards)
    theta = - math.pi / 2

    # define movements to walk in a particular direction
    # step position 2, tripod 1 in upper mid position, tripod 2 in lower mid position
    hexyTripod1GlobalOffset(0,0,-14)
    hexyTripod2GlobalOffset(0,0,0)
    time.sleep(0.2)
    # step position 3, tripod 1 in rear position, tripod 2 in forward position
    hexyTripod1GlobalOffset(math.sin(theta)*s,-math.cos(theta)*s,0)
    hexyTripod2GlobalOffset(-math.sin(theta)*s,math.cos(theta)*s,0)
    time.sleep(0.2)
    # step position 4, tripod 1 in lower mid position, tripod 2 in upper mid position
    hexyTripod1GlobalOffset(0,0,0)
    hexyTripod2GlobalOffset(0,0,-14)
    time.sleep(0.2)
    # step position 1, tripod 1 in forward position, tripod 2 in rear position
    hexyTripod1GlobalOffset(-math.sin(theta)*s,math.cos(theta)*s,0)
    hexyTripod2GlobalOffset(math.sin(theta)*s,-math.cos(theta)*s,0)
    time.sleep(0.2)
    # step position 2, tripod 1 in upper mid position, tripod 2 in lower mid position
    hexyTripod1GlobalOffset(0,0,-14)
    hexyTripod2GlobalOffset(0,0,0)
    time.sleep(0.2)
    hexyGlobalOffset(0,0,0)

#######################################
#      start main program flow        #
#######################################
print "starting sign name"
userName = tkSimpleDialog.askstring("Write Name", "Name for Hexy to write: ")
#userName = "Hexy"

print "Name as entered: ", userName

# scale factor for letters
sf = 25

# loop through each letter of string
for c in userName:
    print "Next letter: ", c
    # call letterPath function
    letterRoute =  letterPath(c)
    # move Hexy along paths
    for i in range(len(letterRoute[0])):
        #print letterRoute[0][i],letterRoute[1][i],letterRoute[2][i]
        hexyGlobalOffset(sf*letterRoute[0][i],sf*letterRoute[1][i],letterRoute[2][i])
        time.sleep(0.1)
    # shuffle to right one letter space
    moveLetterWidthRight(sf*0.2)


