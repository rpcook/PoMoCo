import time
import math
from ikLibrary import * # Inverse-Kinematic Library developed by Rob Cook, information on http://robcook.eu

# scale factor (distance from neutral in step direction)
s=23
# direction (CCW from forwards)
theta = - math.pi / 4

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











