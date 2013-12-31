# TODO finish testing this code. Not reliable as it should be.
import time
import random
from Tkinter import *

exploreGUI = Tk()

def explore():
    print "Calling explore loop."

    # send ping command
    hexy.con.serialHandler.recieveQueue = [] # clear queue
    hexy.con.serialHandler.sendLock.acquire()
    hexy.con.serialHandler.sendQueue.append("S") # ask for arc of distance measurements
    hexy.con.serialHandler.sendLock.release()

    # error handler to catch bad serial data returned
    try:
        # read distances from serial port
        i = 0
        while (hexy.con.serialHandler.recieveQueue == 0) or (i < 20):
            time.sleep(0.1)
            i += 1
        dist = range(9)
        for i in range(9):
            if hexy.con.serialHandler.recieveQueue > 0:
                dist[i] = float(hexy.con.serialHandler.recieveQueue.pop(0))

        # get averages of distances in left, right and forwards directions
        distAvg = range(3)
        distAvg[0] = (dist[0] + dist[1] + dist[2]) / 3 # right
        distAvg[1] = (dist[3] + dist[4] + dist[5]) / 3 # forwards
        distAvg[2] = (dist[6] + dist[7] + dist[8]) / 3 # left

        # check if distance is less than some threshold
        if min(distAvg) < 7:
            print "Too close to something: turn"
            # need to not go forwards to avoid collision
            if min(distAvg) == distAvg[0]: 
                # obstacle to the right
                print "Obstacle on right; turning left"
                move('RotateLeft')
            elif min(distAvg) == distAvg[2]:
                # obstacle to the left
                print "Obstacle on left: turning right"
                move('RotateRight')
            else:
                # obstacle to the front, turn randomly
                print "Obstacle ahead, turning"
                x = random.randint(1,2)
                if x == 1:
                    move('RotateLeft')
                elif x == 2:
                    move('RotateRight')
        else:
            print "Able to continue straight on"
            # wander onwards, possibly randomly turn
            x = random.randint(1,8) # number between 1 and 8
            if x == 1:
                # if x = 1 (1 in 8 chance) turn randomly
                y = random.randint(1,2)
                if y == 1:
                    move('RotateLeft')
                elif y == 2:
                    move('RotateRight')
            else:
                move('MoveForward') # otherwise carry on straighforwards

    except:
        # error detected, repeat loop
        print "Error reading serial port. Trying scan again."

    exploreGUI.after(100,explore)  # reschedule event

# create label in GUI
w = Label(exploreGUI, text="\nHexy is exploring. Close this window to stop.\n")
w.pack()

# schedule task
exploreGUI.after(100,explore)

# start GUI
exploreGUI.mainloop()
