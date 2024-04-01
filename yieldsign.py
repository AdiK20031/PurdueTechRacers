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
    #runs yield sign function for every image needed
    for i in range(0, outputNum):
        yield_sign(qlabs, i, RandOrNot, runName)


def yield_sign(qlabs, outputNum, RandOrNot, runName):

    #destroys previous yield sign 
    qlabs.destroy_all_spawned_actors()
   
    
    #checks user decision
    if RandOrNot == 0:
        #asks for input if user doesn't want input
        X = float(input('Enter X Value: '))
        Y = float(input('Enter Y Value: '))
        roadWidth = float(input('Enter road width where the car is: '))
        distanceFromSign = float(input('How far away should the camera be from the yield sign: '))
        Rotation = int(input('What is the rotation of the yield sign? (1 for none, 2 for pi/2, 3 pi, 4 for 3pi/2) '))
    #Generate random numbers
    elif RandOrNot == 1:
        X = rand.randint(-250,250)
        Y = rand.randint(-250,250)
        roadWidth = rand.uniform(1.5,2)
        distanceFromSign = rand.uniform(1.5,7)
        Rotation = 2
    #Width of the road, basically asks where the center of the car is
    
    #How far away is the car from the yield sign
    
    #Asks the user for the rotation of the yield sign
    
    #Generates the yield sign object
    stop = QLabsYieldSign(qlabs)
    #Generate the camera object
    yieldSignCamera = QLabsFreeCamera(qlabs)
    #Locates where the yield sign is and slightly changes the angle randomly
    angleToYieldSign = math.atan(roadWidth/distanceFromSign) + rand.uniform(-math.pi/4, math.pi/4)

    #If Else loop that changes camera orientation based on the rotation of the sign
    if(Rotation == 1):
        #Spawns in camera object
        yieldSignCamera.spawn_id(actorNumber=1, location=[X+distanceFromSign, Y+roadWidth, 2], rotation=[0, 0, math.pi + angleToYieldSign])
        #Spawns in yield sign object
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, 0], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        #Possesses camera
        yieldSignCamera.possess()
    elif(Rotation == 2):
        yieldSignCamera.spawn_id(actorNumber=1, location=[X+roadWidth, Y+distanceFromSign, 2], rotation=[0, 0, ((3 * math.pi)/2) - angleToYieldSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        yieldSignCamera.possess()
        yieldSignCamera.set_image_capture_resolution(256, 256)
        yieldsignimage = yieldSignCamera.get_image()
    elif(Rotation == 3):
        yieldSignCamera.spawn_id(actorNumber=1, location=[X-distanceFromSign, Y-roadWidth, 2], rotation=[0, 0, angleToYieldSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, math.pi], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        yieldSignCamera.possess()
    elif(Rotation == 4):
        yieldSignCamera.spawn_id(actorNumber=1, location=[X-roadWidth, Y-distanceFromSign, 2], rotation=[0, 0, math.pi/2 - angleToYieldSign])
        stop.spawn_id(actorNumber=1, location=[X, Y, 0.0], rotation=[0,0, (3 * math.pi)/2], scale=[1,1,1], configuration=0, waitForConfirmation=True)
        yieldSignCamera.possess()


    # collecting the world transform coordinates of the yield sign

    x, loc, rot, scale = stop.get_world_transform()

    print(x, loc, rot, scale)


    # pinging existing sign - this should return True if we printed it

    stop.ping()

    # waits so we can see the output

    time.sleep(1)
    
    #gets the array element in the tuple from get.image()
    YieldSignImage = yieldsignimage[1]
    #converts array to np array
    YieldSignImageArray = np.array(YieldSignImage)
    #converts to RGB
    YieldSignImageArrayRGB = cv2.cvtColor(YieldSignImageArray, cv2.COLOR_BGR2RGB)

    #generates image
    img = Image.fromarray(YieldSignImageArrayRGB)

    #saves image
    #img.save("yieldsigns\output"+ str(outputNum)  + runName + ".png")
    
    IMAGE_STORAGE= "C:\\Users\\matth\\Documents\\QCar Images\\yield"

    fname = "\\yield_sign_" + str(outputNum) + ".png"
    
    img.save(IMAGE_STORAGE+fname)


    

if __name__ == "__main__":

    main()
