import sys

import math

import time

import random as rand


from qvl.qlabs import QuanserInteractiveLabs

from qvl.free_camera import QLabsFreeCamera

from qvl.crosswalk import QLabsCrosswalk

from qvl.roundabout_sign import QLabsRoundaboutSign

from qvl.yield_sign import QLabsYieldSign

from qvl.stop_sign import QLabsStopSign

from qvl.traffic_cone import QLabsTrafficCone

from qvl.traffic_light import QLabsTrafficLight

def main():


    # creates a server connection with Quanser Interactive Labs and manages the communications

    qlabs = QuanserInteractiveLabs()


    print("Connecting to QLabs...")

    # trying to connect to QLabs and open the instance we have created - program will end if this fails

    try:

        qlabs.open("localhost")

    except:

        print("Unable to connect to QLabs")

        return


    qlabs.destroy_all_spawned_actors()
    
    stop_sign(qlabs)


def stop_sign(qlabs):

    
    #This code asks the user if they want random coordinate generation
    RandOrNot = int(input('Do you want random coordinate generation? 0 or 1. This may generate signs on the road in City or Cityscape but has no issues on Studio: '))
    #If the user doesn't want random generation ask for input
    if RandOrNot == 0:
        X = float(input('Enter X Value: '))
        Y = float(input('Enter Y Value: '))
    #Generate random numbers
    elif RandOrNot == 1:
        X = rand.randint(-250,250)
        Y = rand.randint(-250,250)
    #Width of the road, basically asks where the center of the car is
    roadWidth = float(input('Enter road width where the car is: '))
    #How far away is the car from the stop sign
    distanceFromSign = float(input('How far away should the camera be from the stop sign: '))
    #Asks the user for the rotation of the stop sign
    Rotation = int(input('What is the rotation of the stop sign? (1 for none, 2 for pi/2, 3 pi, 4 for 3pi/2) '))
    #Generates the stop sign object
    stop = QLabsStopSign(qlabs)
    #Generate the camera object
    stopSignCamera = QLabsFreeCamera(qlabs)
    #Locates where the stop sign is and slightly changes the angle randomly
    angleToStopSign = math.atan(roadWidth/distanceFromSign) + rand.uniform(-math.pi/4, math.pi/4)

    #If Else loop that changes camera orientation based on the rotation of the sign
    if(Rotation == 1):
        #Spawns in camera object
        stopSignCamera.spawn_id(actorNumber=1, location=[X+distanceFromSign, Y+roadWidth, 2], rotation=[0, 0, math.pi + angleToStopSign])
        #Spawns in stop sign object
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, 0], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        #Possesses camera
        stopSignCamera.possess()
    elif(Rotation == 2):
        stopSignCamera.spawn_id(actorNumber=1, location=[X+roadWidth, Y+distanceFromSign, 2], rotation=[0, 0, ((3 * math.pi)/2) - angleToStopSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        stopSignCamera.possess()
    elif(Rotation == 3):
        stopSignCamera.spawn_id(actorNumber=1, location=[X-distanceFromSign, Y-roadWidth, 2], rotation=[0, 0, angleToStopSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        stopSignCamera.possess()
    elif(Rotation == 4):
        stopSignCamera.spawn_id(actorNumber=1, location=[X-roadWidth, Y-distanceFromSign, 2], rotation=[0, 0, math.pi/2 - angleToStopSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, (3 * math.pi)/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        stopSignCamera.possess()


    # collecting the world transform coordinates of the stop sign

    x, loc, rot, scale = stop.get_world_transform()

    print(x, loc, rot, scale)


    # pinging existing sign - this should return True if we printed it

    stop.ping()

    # waits so we can see the output

    time.sleep(1)



if __name__ == "__main__":

    main()
