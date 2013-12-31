import time
import math

# neutral position definintion
neuZ = -85
neuY = 110
neuX = 110
neuXmid = 150

# modified to use the servotorComm binary communication protocol (developed by forum user michal: http://forum.arcbotics.com/memberlist.php?mode=viewprofile&u=771). NB requires updated software on Hexy's Ardiuno controller too. If you don't have these, please use ikLibrary.py instead. Step speed will be limited.

# define Inverse Kinematic function for lower leg joints
# variable definitions: http://robcook.eu/hexy/inverse-kinematics-part-1/
def ikLowerLeg(x, y):
    #print "IK function called. x=", x, "y=", y
    a = 49.0
    b = 52.0
    try:
        d = math.sqrt(x*x+y*y)
        k = (d*d-b*b+a*a)/(2*d)
        m = math.sqrt(a*a-k*k)
    except ZeroDivisionError:
        print "Divide by Zero error. No valid joint solution."
        return
    except ValueError:
        print "Math function error. Probably square root of negative number. No valid joint solution."
        return
    theta = math.degrees(math.atan2(float(y),float(x))-math.atan2(m,k))
    phi   = -math.degrees(math.atan2(m,k)+math.atan2(m,(d-k)))
    returnAngles = [theta, phi]
    #print "theta=", theta, "phi=", phi
    return returnAngles        

# define Inverse Kinematic function for full leg
# variable definitions: http://robcook.eu/hexy/inverse-kinematics-part-3-full-leg-solution/
def ikFullLeg(x, y, z):
    alpha = math.degrees(math.atan2(y, x))
    lowerLegAngles = ikLowerLeg(math.sqrt(x*x+y*y)-26.0, z)
    #print "ikFullLeg ", alpha, lowerLegAngles[0], lowerLegAngles[1]
    returnAngles = [alpha, lowerLegAngles[0], lowerLegAngles[1]] 
    return returnAngles

# move LF leg in global co-ordinate system
def hexyLFleg(x,y,z):
    #print "LF leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x + 65.8
    y = y - 76.3
    # rotate to leg zero position
    legx=math.cos(-2.2829)*x-math.sin(-2.2829)*y
    legy=math.sin(-2.2829)*x+math.cos(-2.2829)*y
    # get IK solution and move leg
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.con.servos[7].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[6].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[5].setPos(deg=legAngles[2], move=False)
    
# move LM leg in global co-ordinate system
def hexyLMleg(x,y,z):
    #print "LM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = -(x + 103.3)
    y = -y
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.con.servos[11].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[10].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[9].setPos(deg=legAngles[2], move=False)
    
# move LB leg in global co-ordinate system
def hexyLBleg(x,y,z):
    #print "LB leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x + 65.8
    y = y + 76.3
    # rotate to leg zero position
    legx=math.cos(2.2829)*x-math.sin(2.2829)*y
    legy=math.sin(2.2829)*x+math.cos(2.2829)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.con.servos[15].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[14].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[13].setPos(deg=legAngles[2], move=False)
    
# move RF leg in global co-ordinate system
def hexyRFleg(x,y,z):
    #print "RF leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 65.8
    y = y - 76.3
    # rotate to leg zero position
    legx=math.cos(-0.8587)*x-math.sin(-0.8587)*y
    legy=math.sin(-0.8587)*x+math.cos(-0.8587)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.con.servos[24].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[25].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[26].setPos(deg=legAngles[2], move=False)
    
# move RM leg in global co-ordinate system
def hexyRMleg(x,y,z):
    #print "RM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 103.3
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.con.servos[20].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[21].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[22].setPos(deg=legAngles[2], move=False)
    
# move RB leg in global co-ordinate system
def hexyRBleg(x,y,z):
    #print "RB leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 65.8
    y = y + 76.3
    # rotate to leg zero position
    legx=math.cos(0.8587)*x-math.sin(0.8587)*y
    legy=math.sin(0.8587)*x+math.cos(0.8587)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.con.servos[16].setPos(deg=legAngles[0], move=False)
    hexy.con.servos[17].setPos(deg=legAngles[1], move=False)
    hexy.con.servos[18].setPos(deg=legAngles[2], move=False)
    
# apply rotation to x-y co-ords about z-axis (z-angle in radians)
def rotZ(x,y,z):
    rotX = x * math.cos(z) - y * math.sin(z)
    rotY = x * math.sin(z) + y * math.cos(z)
    returnAngles = [rotX, rotY]
    return returnAngles
    
# move Hexy to position relative to "neutral" position
def hexyGlobalOffset(x,y,z):
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)

# move Hexy to position relative to "neutral" position
def hexyTripod1GlobalOffset(x,y,z):
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
 
# move Hexy to position relative to "neutral" position
def hexyTripod2GlobalOffset(x,y,z):
    # move hexy to a position relative to "neutral"
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)
    
# move Hexy to position relative to "neutral" position, plus z-rotation
def hexyGlobalOffsetRot(x,y,z,rtZ):
    # move hexy to a position relative to "neutral"
    rtdCrds = rotZ(-neuX-x, neuY-y, rtZ)
    hexyLFleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(-neuXmid-x, -y, rtZ)
    hexyLMleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(-neuX-x, -neuY-y, rtZ)
    hexyLBleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuX-x, neuY-y, rtZ)
    hexyRFleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuXmid-x, -y, rtZ)
    hexyRMleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuX-x, -neuY-y, rtZ)
    hexyRBleg(rtdCrds[0], rtdCrds[1], neuZ-z)

# move Hexy to position relative to "neutral" position, plus z-rotation
def hexyTripod1GlobalOffsetRot(x,y,z,rtZ):
    # move hexy to a position relative to "neutral"
    rtdCrds = rotZ(-neuX-x, neuY-y, rtZ)
    hexyLFleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(-neuX-x, -neuY-y, rtZ)
    hexyLBleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuXmid-x, -y, rtZ)
    hexyRMleg(rtdCrds[0], rtdCrds[1], neuZ-z)
 
# move Hexy to position relative to "neutral" position, plus z-rotation
def hexyTripod2GlobalOffsetRot(x,y,z,rtZ):
    # move hexy to a position relative to "neutral"
    rtdCrds = rotZ(-neuXmid-x, -y, rtZ)
    hexyLMleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuX-x, neuY-y, rtZ)
    hexyRFleg(rtdCrds[0], rtdCrds[1], neuZ-z)
    rtdCrds = rotZ(neuX-x, -neuY-y, rtZ)
    hexyRBleg(rtdCrds[0], rtdCrds[1], neuZ-z)

