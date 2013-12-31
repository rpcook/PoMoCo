from Tkinter import *
from tkFileDialog   import askopenfile
from tkFileDialog   import askopenfilename
from tkFileDialog   import asksaveasfile
from tkFileDialog   import asksaveasfilename

import os
import ConfigParser
from servotorComm import runMovement

FPS = 10

class App:
    
    def __init__(self, master, controller):
        self.con = controller
        self.master = master

        self.frame = Frame(self.master)

        self.frame.pack()

        #setup menu system
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)

        menu.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="New")
        #filemenu.add_command(label="Save Offsets", command=self.saveOffsets)
        
        # TODO: bring these over from servitorGui
        #filemenu.add_command(label="Open Offsets", command=self.openOffsets)
        #filemenu.add_command(label="Save Positions", command=self.savePositions)
        #filemenu.add_command(label="Open Positions", command=self.openPositions)

        #filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quitApp)

        #setup kill button
        #self.killButton = Button(self.frame, text="Kill All Servos",fg="red",
        #                        font=("Helvetica", 12),command=self.estop)
        #self.killButton.grid(row=0,column=4)
        
        #arrays for icons, commands
        iconList = ["move_fwdleft.gif", "move_left.gif", "move_backleft.gif", "move_fwds.gif", "stop.gif", "move_back.gif", "move_fwdright.gif", "move_right.gif", "move_backright.gif", "rotate_ccw.gif", "rotate_cw.gif", "dance.gif", "sixaxis.gif", "sign_hexy.gif", "sign_name.gif"]
        commandList = ["crab_fwdleft", "crab_left", "crab_backleft", "crab_fwd", "", "crab_back", "crab_fwdright", "crab_right", "crab_backright", "RotateLeft", "RotateRight", "dance_random", "SixAxisBinary", "sign_hexy", "sign_name"]
        
        #draw all the buttons and add icons/ commands
        counter = 0
        for icons in iconList:
            b = Button(self.frame)
            b.icon = PhotoImage(file="./Icons/" + icons)
            b.config(image=b.icon, width="150", height="150")
            b.move_name = commandList[counter]
            # modified command if the command is Stop
            if b.move_name=="":
                b.config(command = self.estop)
            elif b.move_name=="sign_name":
                b.sel = lambda b = b: move(b.move_name)
                b.config(command = b.sel)
            else:
                b.sel = lambda b = b: runMovement(move,b.move_name)
                b.config(command = b.sel)
            b.grid(row=(counter%3)*2+2, column=(counter/3)*2)
            #b.pack()
            counter += 1
            
        """
        for icons in iconList:
            b = Button(self.frame)
            b.icon = PhotoImage(file="./Icons/" + icons)
            b.config(image=b.icon, width="150", height="150")
            b.move_name = commandList[counter]
            b.sel = lambda b = b: runMovement(move,b.move_name)
            # exception if the command is Stop
            if b.move_name=="":
                b.config(command = self.estop)
            #elif b.move_name=="sign_name":
                #b.config(command = execfile("./DemoMoves/sign_name.py"))
            else:
                b.config(command = b.sel)
            b.grid(row=(counter%3)*2+2, column=(counter/3)*2)
            #b.pack()
            counter += 1
        """
        """
        #fwd left
        self.fwdLeftPhoto = PhotoImage(file="./Icons/move_fwdleft.gif")
        self.fwdLeftButton = Button(self.frame)
        #self.fwdLeftButton.move_name = "crab_fwdleft"
        #self.fwdLeftButton.sel = lambda self.fwdLeftButton = self.fwdLeftButton: runMovement(move, self.fwdLeftButton.move_name)
        #self.fwdLeftButton.config(image=self.fwdLeftPhoto, width="150", height="150", command = self.fwdLeftButton.sel)
        self.fwdLeftButton.func = lambda func = func: runMovement(move,"crab_fwdleft")
        self.fwdLeftButton.config(image=self.fwdLeftPhoto, width="150", height="150", command=self.fwdLeftButton.func)
        self.fwdLeftButton.grid(row=2, column=0)
        #fwd 
        self.fwdPhoto = PhotoImage(file="./Icons/move_fwds.gif")
        self.fwdButton = Button(self.frame)
        self.fwdButton.config(image=self.fwdPhoto, width="150", height="150")
        self.fwdButton.grid(row=2, column=2)
        #fwd right
        self.fwdRightPhoto = PhotoImage(file="./Icons/move_fwdright.gif")
        self.fwdRightButton = Button(self.frame)
        self.fwdRightButton.config(image=self.fwdRightPhoto, width="150", height="150")
        self.fwdRightButton.grid(row=2, column=4)
        #left
        self.leftPhoto = PhotoImage(file="./Icons/move_left.gif")
        self.leftButton = Button(self.frame)
        self.leftButton.config(image=self.leftPhoto, width="150", height="150")
        self.leftButton.grid(row=4, column=0)
        #stop
        self.stopPhoto = PhotoImage(file="./Icons/stop.gif")
        self.stopButton = Button(self.frame, command=self.estop)
        self.stopButton.config(image=self.stopPhoto, width="150", height="150")
        self.stopButton.grid(row=4, column=2)
        #right
        self.rightPhoto = PhotoImage(file="./Icons/move_right.gif")
        self.rightButton = Button(self.frame)
        self.rightButton.config(image=self.rightPhoto, width="150", height="150")
        self.rightButton.grid(row=4, column=4)
        #back left
        self.backLeftPhoto = PhotoImage(file="./Icons/move_backleft.gif")
        self.backLeftButton = Button(self.frame)
        self.backLeftButton.config(image=self.backLeftPhoto, width="150", height="150")
        self.backLeftButton.grid(row=6, column=0)
        #back
        self.backPhoto = PhotoImage(file="./Icons/move_back.gif")
        self.backButton = Button(self.frame)
        self.backButton.config(image=self.backPhoto, width="150", height="150")
        self.backButton.grid(row=6, column=2)
        #back right
        self.backRightPhoto = PhotoImage(file="./Icons/move_backright.gif")
        self.backRightButton = Button(self.frame)
        self.backRightButton.config(image=self.backRightPhoto, width="150", height="150")
        self.backRightButton.grid(row=6, column=4)
        
        #rotate left
        self.rotLeftPhoto = PhotoImage(file="./Icons/rotate_ccw.gif")
        self.rotLeftButton = Button(self.frame)
        self.rotLeftButton.config(image=self.rotLeftPhoto, width="150", height="150")
        self.rotLeftButton.grid(row=2, column=6)
        #rotate right
        self.rotRightPhoto = PhotoImage(file="./Icons/rotate_cw.gif")
        self.rotRightButton = Button(self.frame)
        self.rotRightButton.config(image=self.rotRightPhoto, width="150", height="150")
        self.rotRightButton.grid(row=4, column=6)        
        #dance
        self.dancePhoto = PhotoImage(file="./Icons/dance.gif")
        self.danceButton = Button(self.frame)
        self.danceButton.config(image=self.dancePhoto, width="150", height="150")
        self.danceButton.grid(row=6, column=6)        

        #sign stylised "X"
        self.signxPhoto = PhotoImage(file="./Icons/sign_x.gif")
        self.signxButton = Button(self.frame)
        self.signxButton.config(image=self.signxPhoto, width="150", height="150")
        self.signxButton.grid(row=2, column=8)        
        #sign Hexy
        self.signHexyPhoto = PhotoImage(file="./Icons/sign_hexy.gif")
        self.signHexyButton = Button(self.frame)
        self.signHexyButton.config(image=self.signHexyPhoto, width="150", height="150")
        self.signHexyButton.grid(row=4, column=8)        
        #write name
        self.writeNamePhoto = PhotoImage(file="./Icons/sign_name.gif")
        self.writeNameButton = Button(self.frame)
        self.writeNameButton.config(image=self.writeNamePhoto, width="150", height="150")
        self.writeNameButton.grid(row=6, column=8)
        """ 

        self.addSpace([1, 1])
        self.addSpace([3, 3])
        self.addSpace([5, 5])
        self.addSpace([7, 5])
        
        self.loadOffsets()

        # TODO add code to make sensible looking GUI
        # required buttons: fwds, bkwds, left, right, (diagonals?), turn_cw, turn_ccw
        # special buttons: sign Hexy (X?), sign custom message (requires dialog box)
        # stretch commands: modulate height, modulate body angles

        self.servos = []
        # remove code for slider generation
        """
        #setup left side, 4 groups of 4 servo controls
        for i in xrange(4):
            self.newServo(0+i*4,[1,8+i*5])
            self.newServo(1+i*4,[1,9+i*5])
            self.newServo(2+i*4,[1,10+i*5])
            self.newServo(3+i*4,[1,11+i*5])
            #self.addSpace([0,12+i*5])

        #setup right side, 4 groups of 4 servo controls
        for i in xrange(4):
            self.newServo(16+i*4,[11,8+i*5])
            self.newServo(17+i*4,[11,9+i*5])
            self.newServo(18+i*4,[11,10+i*5])
            self.newServo(19+i*4,[11,11+i*5])
            #self.addSpace([11,12+i*5])
        """
        #add some spaces for asthetics
        #self.addSpace([10,10])
        

        # generate buttons for all move functions
        """
        counter = 0
        for move_name in moves:
            b = Button(self.frame, text=move_name, font=("Helvetica", 7))
            b.move_name = move_name
            b.sel = lambda b = b: runMovement(move,b.move_name)
            b.config(command = b.sel)
            b.grid(row=counter+8, column=0)
            #b.pack()
            counter += 1
        """

        # don't need the following line as there are no sliders to update
        #self.poll()
        self.estop()

    def saveOffsets(self):
        cfgFile = asksaveasfile(filetypes = [('CFG', '*.cfg'),("All Files",".*")], defaultextension=".cfg")
        config = ConfigParser.ConfigParser()
        config.add_section("offsets")
        for servo in self.servos:
            offset = int(servo.offset.get().strip("+"))
            config.set("offsets", "%.3d"%(servo.servoNum), offset)
        config.write(cfgFile)

    def quitApp(self):
        root.quit()

    """
    def poll(self):
        # Constantly updates the gui based on the current status of the controller

        for servo in self.con.servos:
            pos = self.con.servos[servo].getPosuS()
            self.servos[servo].servoPos.set(pos)

            offset = self.con.servos[servo].getOffsetuS()
            self.servos[servo].offset.set(offset)

            active = self.con.servos[servo].getActive()
            if active:
                self.servos[servo].active.set(1)
            else:
                self.servos[servo].active.set(0)

        self.master.after(1000/FPS, self.poll)
    """

    def addSpace(self,coords):
        l2 = Label(self.frame, text="   ", fg="red")
        #l2 = Label(self.frame, text="\t\t", fg="red")
        l2.pack()
        l2.grid(row=coords[1], column=coords[0])

    def newServo(self,servoNum,coords):
        self.servos.append(servoGroup(self.frame,self.con,servoNum,colX=coords[0],rowY=coords[1]))

    def loadOffsets(self):
        # If there is one offset file in the folder, automatically load it
        off_files = []
        for filename in os.listdir(os.getcwd()):
            start, ext = os.path.splitext(filename)
            if ext == '.cfg':
                off_files.append(filename)

        if len(off_files) == 1:
            print "opening",off_files[0]
            config = ConfigParser.ConfigParser()
            config.read(off_files[0])

            try:
                offsets = config.items('offsets')
                for offset in offsets:
                    servoNum = int(offset[0])
                    offset = int(offset[1])
                    for servo in self.con.servos:
                        if self.con.servos[servo].servoNum == servoNum:
                            #print "set servo",servoNum,"offset as",offset
                            self.con.servos[servo].setOffset(timing=offset)
                            break
                print "automatically loaded offsets from",off_files[0]
            except:
                print "automatic offset load failed, is there an offset file in the program directory?"

    def estop(self):
        self.con.killAll()
        
class servoGroup:
    def __init__(self,frame,con,servoNum,servoPos=1500,rowY=0,colX=0):
        self.frame = frame
        self.con = con
        self.frame.pack()

        self.v = IntVar()
        self.v.set(int(servoPos))
        self.active = IntVar()
        self.active.set(0)
        self.servoPos = IntVar()
        self.servoPos.set(servoPos)
        self.servoNum = servoNum

        offset = self.con.servos[self.servoNum].getOffsetuS()
        self.offset = StringVar()
        self.offset.set(int(offset))

        self.servoLabel = Label(self.frame, text="Servo %.2d"%(servoNum), font=("Helvetica", 7))
        self.servoLabel.grid(row=rowY, column=0+colX)

        self.onCheck = Checkbutton(self.frame, text="On", var=self.active,command=self.checkServo, font=("Helvetica", 7))
        self.onCheck.grid(row=rowY, column=1+colX)

        self.resetButton = Button(self.frame, text="Reset",command=self.resetServo, font=("Helvetica", 7))
        self.resetButton.grid(row=rowY, column=2+colX)


        self.posScale = Scale(self.frame, from_=500, to=2500, length=155, resolution=10,
                                orient=HORIZONTAL,showvalue=0,var=self.servoPos,command=self.moveServo)
        self.posScale.grid(row=rowY, column=3+colX)


        self.servoPosLabel = Label(self.frame,textvariable=self.servoPos, font=("Helvetica", 7))
        self.servoPosLabel.grid(row=rowY, column=4+colX)

        #offset label
        self.servoOffsetLabel = Label(self.frame,textvariable=self.offset, font=("Helvetica", 7))
        self.servoOffsetLabel.grid(row=rowY, column=5+colX)

        #offset plus
        self.offsetIncButton = Button(self.frame, text="+",command=self.offsetInc, font=("Helvetica", 7))
        self.offsetIncButton.grid(row=rowY, column=6+colX)

        #offset minus
        self.offsetDecButton = Button(self.frame, text="-",command=self.offsetDec, font=("Helvetica", 7))
        self.offsetDecButton.grid(row=rowY, column=7+colX)

    def checkServo(self):
        if self.active.get() == 0:
            self.active.set(0)
            self.con.servos[self.servoNum].kill()
            #print "Servo",self.servoNum,"activated"
        else:
            self.active.set(1)
            pos = self.servoPos.get()
            self.con.servos[self.servoNum].setPos(timing = pos)

            #print "Servo",self.servoNum,"killed"

    def moveServo(self,newServoPos):
        if self.active.get():
            self.con.servos[self.servoNum].setPos(int(newServoPos))
            self.con.servos[self.servoNum].move()
            self.servoPos.set(int(newServoPos))
            self.v.set(int(newServoPos))
        #print "set servo",self.servoNum,"to",newServoPos

    def resetServo(self):
        #print "reset servo",self.servoNum
        self.con.servos[self.servoNum].reset()

    def offsetInc(self):
        offset = self.con.servos[self.servoNum].getOffsetuS()
        self.con.servos[self.servoNum].setOffset(timing=offset+10)
        self.offset.set(offset+10)
        #print "servo",self.servoNum,"offset increased to",self.offset

        self.con.servos[self.servoNum].move()

    def offsetDec(self):
        offset = self.con.servos[self.servoNum].getOffsetuS()
        self.con.servos[self.servoNum].setOffset(timing=offset-10)
        self.offset.set(offset-10)
        #print "servo",self.servoNum,"offset increased to",self.offset
        self.con.servos[self.servoNum].move()

def startGUI(controller):
    global root 
    root = Tk()

    global app
    app = App(root,controller)
    root.mainloop()
    
    
