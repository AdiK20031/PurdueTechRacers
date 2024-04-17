# author:Yu-Hung Wang
# Date: 04/01/2024
# Description: This code generates images that contains traffic lights in qlab.

# Library used 
import math
import numpy as np
import random as rand
from PIL import Image
import cv2
# qlab library
from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.traffic_light import QLabsTrafficLight

# Global variable for the program
IMAGE_SIZE = [250, 250] # [width, height]
IMAGE_STORAGE = "C:\\Users\\thoma\PurdueTechRacers\\Generated_Image\\traffic_light"
IMAGE_COUNT = 50 # the number of image you want

# Camera angle settings
CAMERA_ANGLE = np.array([[0,-math.pi/18,-math.pi/2],
                          [0,-math.pi/18,math.pi/2],
                          [0,-math.pi/18,-math.pi/2],
                          [0,-math.pi/18,math.pi/2]
                          ])
# camera distance offset
CAMERA_BASE_OFFSET = np.array([[-2.5,-4.5,-1.5],  
                          [2.5, 4.5,-1.5],      
                          [-2.5,-4.5,-1.5],      
                          [2.5, 4.5,-1.5] 
                          ])

# traffic light orientation and position in the map
LIGHT_ROTATIONS = np.array([[0,0,math.pi],
                            [0,0,0],
                            [0,0,math.pi],
                            [0,0,0]
                            ])
# traffic light corodinate on the map
LIGHT_CORDINATES = np.array([[-22,7.336,0.071],
                            [4.619,2,0.071],
                            [-2,16.580,0.071],
                            [24.609,4.281,0.071]
                            ])

#spawn camera in the sence
def spawnCamera(camera,pos, rota):
    camera.spawn(location=pos, rotation=rota)
    camera.possess()

#spawn traffic light in the sence
def spawnTrafficLight(light, camera ,pos, rota):
    # spawn a traffic light
    lightState = rand.randint(0,2)

    print(lightState)
    if lightState == 0:
        print("red")
        light.set_state(state=light.STATE_RED,waitForConfirmation=True)
    elif lightState == 1:
        light.set_state(state=light.STATE_GREEN,waitForConfirmation=True)
    else:
        light.set_state(state=light.STATE_YELLOW,waitForConfirmation=True)
    
    light.spawn_id(actorNumber=1, location=pos, rotation=rota, scale=[1,1,1], configuration=0, waitForConfirmation=True)

    # setting camer resolution
    camera.set_image_capture_resolution(width = IMAGE_SIZE[0], height = IMAGE_SIZE[1])
    img =  camera.get_image()   # get image as an array
    light.destroy()
    
    return img

# this where the program is excuting
def main():
    # some intialization
    qlabs = QuanserInteractiveLabs()
    camera0 = QLabsFreeCamera(qlabs)
    light = QLabsTrafficLight(qlabs)

    try:
        qlabs.open("localhost")
    except:
        print("Unable to connect to QLabs")
        return

    qlabs.destroy_all_spawned_actors()
    
    for i in range(IMAGE_COUNT):
        distanceMod = -1
        posCode = rand.randint(0,3)
        
        if posCode == 1 or posCode == 3:
            distanceMod = 1

        # generating a random camera angle offset
        cameraAngleOffset = [0,0,math.pi/6*rand.randint(-100,100)/100]
        # generating a random camera distance offset from the traffic light
        cameraOffset = CAMERA_BASE_OFFSET[posCode] + [rand.random()-0.5, (distanceMod)*3*rand.random(),0]
        
        spawnCamera(camera0,LIGHT_CORDINATES[posCode]-cameraOffset, CAMERA_ANGLE[posCode]+cameraAngleOffset)
        img = spawnTrafficLight(light,camera0,LIGHT_CORDINATES[posCode], LIGHT_ROTATIONS[posCode])

        # seeting the image into right format
        StopSignImage = img[1]
        StopSignImageArray = np.array(StopSignImage)
        StopSignImageArrayRGB = cv2.cvtColor(StopSignImageArray, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(StopSignImageArrayRGB)
        
        # making the name of the file 
        fname = "\\traffic_light_" + str(i) + ".png"
        # building the file
        img.save(IMAGE_STORAGE+fname)


if __name__ == "__main__":
    main()