#Library imports

import sys

import math

import time

import random as rand

import cv2

from PIL import Image

import numpy as np

from qvl.qlabs import QuanserInteractiveLabs

from qvl.free_camera import QLabsFreeCamera

from qvl.crosswalk import QLabsCrosswalk

from qvl.roundabout_sign import QLabsRoundaboutSign

from qvl.yield_sign import QLabsYieldSign

from qvl.stop_sign import QLabsStopSign

from qvl.traffic_cone import QLabsTrafficCone

from qvl.traffic_light import QLabsTrafficLight

#Main function

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


    #names file name for image batch
    runName = str(input('Name this batch of images: '))
    #asks how many images script should generate
    outputNum = int(input('How many images do you want?'))
    #asks user for random numbers
    RandOrNot = int(input('Do you want random coordinate generation? 0 or 1. This may generate signs on the road in City or Cityscape but has no issues on Studio: '))
    #runs traffic_cone sign function for every image needed
    for i in range(0, outputNum):
        traffic_cone(qlabs, i, RandOrNot, runName)


def traffic_cone(qlabs, outputNum, RandOrNot, runName):

    #destroys previous traffic_cone sign 
    qlabs.destroy_all_spawned_actors()
   
    
    #checks user decision
    if RandOrNot == 0:
        #asks for input if user doesn't want input
        X = float(input('Enter X Value: '))
        Y = float(input('Enter Y Value: '))
        roadWidth = float(input('Enter road width where the car is: '))
        distanceFromSign = float(input('How far away should the camera be from the traffic_cone: '))
        Rotation = int(input('What is the rotation of the traffic_cone? (1 for none, 2 for pi/2, 3 pi, 4 for 3pi/2) '))
    #Generate random numbers
    elif RandOrNot == 1:
        X = rand.randint(-250,250)
        Y = rand.randint(-250,250)
        roadWidth = rand.uniform(1.5,2)
        distanceFromSign = rand.uniform(1.5,7)
        Rotation = 2
    #Width of the road, basically asks where the center of the car is
    
    #How far away is the car from the traffic_cone
    
    #Asks the user for the rotation of the traffic_cone
    
    #Generates the traffic_cone object
    stop = QLabsTrafficCone(qlabs)
    #Generate the camera object
    TrafficConeSignCamera = QLabsFreeCamera(qlabs)
    #Locates where the traffic cone is and slightly changes the angle randomly
    angleToTrafficCone = math.atan(roadWidth/distanceFromSign) + rand.uniform(-math.pi/4, math.pi/4)

    #If Else loop that changes camera orientation based on the rotation of the sign
    if(Rotation == 1):
        #Spawns in camera object
        TrafficConeSignCamera.spawn_id(actorNumber=1, location=[X+distanceFromSign, Y+roadWidth, 2], rotation=[0, 0, math.pi + angleToTrafficCone])
        #Spawns in traffic cone object
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, 0], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        #Possesses camera
        TrafficConeSignCamera.possess()
    elif(Rotation == 2):
        TrafficConeSignCamera.spawn_id(actorNumber=1, location=[X+roadWidth, Y+distanceFromSign, 2], rotation=[0, 0, ((3 * math.pi)/2) - angleToTrafficCone])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        TrafficConeSignCamera.possess()
        TrafficConeSignCamera.set_image_capture_resolution(256, 256)
        trafficconeimage = TrafficConeSignCamera.get_image()
    elif(Rotation == 3):
        TrafficConeSignCamera.spawn_id(actorNumber=1, location=[X-distanceFromSign, Y-roadWidth, 2], rotation=[0, 0, angleToTrafficCone])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        TrafficConeSignCamera.possess()
    elif(Rotation == 4):
        TrafficConeSignCamera.spawn_id(actorNumber=1, location=[X-roadWidth, Y-distanceFromSign, 2], rotation=[0, 0, math.pi/2 - angleToTrafficCone])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, (3 * math.pi)/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        TrafficConeSignCamera.possess()


    # collecting the world transform coordinates of the traffic cone

    x, loc, rot, scale = stop.get_world_transform()

    print(x, loc, rot, scale)


    # pinging existing sign - this should return True if we printed it

    stop.ping()

    # waits so we can see the output

    time.sleep(1)
    
    #gets the array element in the tuple from get.image()
    TrafficConeImage = trafficconeimage[1]
    #converts array to np array
    TrafficConeImageArray = np.array(TrafficConeImage)
    #converts to RGB
    TrafficConeImageArrayRGB = cv2.cvtColor(TrafficConeImageArray, cv2.COLOR_BGR2RGB)

    #generates image
    img = Image.fromarray(TrafficConeImageArrayRGB)

    #saves image
    #img.save("trafficsigns\output"+ str(outputNum)  + runName + ".png")
    
    IMAGE_STORAGE= "C:\\Users\\matth\\Documents\\QCar Images\\traffic_cone"

    fname = "\\traffic_cone_" + str(outputNum) + ".png"
    
    img.save(IMAGE_STORAGE+fname)


    

if __name__ == "__main__":

    main()
