import time
import math

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
    hexy.LF.hip(legAngles[0])
    hexy.LF.knee(legAngles[1])
    hexy.LF.ankle(legAngles[2])
    
# move LM leg in global co-ordinate system
def hexyLMleg(x,y,z):
    #print "LM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = -(x + 103.3)
    y = -y
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.LM.hip(legAngles[0])
    hexy.LM.knee(legAngles[1])
    hexy.LM.ankle(legAngles[2])
    
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
    hexy.LB.hip(legAngles[0])
    hexy.LB.knee(legAngles[1])
    hexy.LB.ankle(legAngles[2])
    
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
    hexy.RF.hip(legAngles[0])
    hexy.RF.knee(legAngles[1])
    hexy.RF.ankle(legAngles[2])
    
# move RM leg in global co-ordinate system
def hexyRMleg(x,y,z):
    #print "RM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 103.3
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.RM.hip(legAngles[0])
    hexy.RM.knee(legAngles[1])
    hexy.RM.ankle(legAngles[2])
    
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
    hexy.RB.hip(legAngles[0])
    hexy.RB.knee(legAngles[1])
    hexy.RB.ankle(legAngles[2])
    
# move Hexy to position relative to "neutral" position
def hexyGlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)

# move Hexy to position relative to "neutral" position
def hexyTripod1GlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
 
# move Hexy to position relative to "neutral" position
def hexyTripod2GlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)

# scale factor (distance from neutral in step direction)
s=23
# direction (CCW from forwards)
theta = math.pi / 4

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











