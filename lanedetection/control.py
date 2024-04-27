# region: package imports
import os
import numpy as np
import random
import sys
import time
import math
import struct
import cv2
import random
#import matplotlib.pyplot as plt
from PIL import Image


# environment objects

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar import QLabsQCar
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape
from qvl.system import QLabsSystem
from qvl.walls import QLabsWalls
from qvl.flooring import QLabsFlooring
from qvl.stop_sign import QLabsStopSign
from qvl.crosswalk import QLabsCrosswalk
#import pal.resources.rtmodels as rtmodels


#endregion

#Function to setup QLabs, Spawn in QCar, and run real time model
def main(initialPosition, initialOrientation, num):
    # Try to connect to Qlabs

    os.system('cls')
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()


    #Set the Workspace Title
    hSystem = QLabsSystem(qlabs)
    x = hSystem.set_title_string('ACC Self Driving Car Competition', waitForConfirmation=True)


    ### Flooring

    x_offset = 0.13
    y_offset = 1.67
    hFloor = QLabsFlooring(qlabs)
    #hFloor.spawn([0.199, -0.491, 0.005])
    hFloor.spawn_degrees([x_offset, y_offset, 0.001],rotation = [0, 0, -90])


    ### region: Walls
    hWall = QLabsWalls(qlabs)
    hWall.set_enable_dynamics(False)

    for y in range (5):
        hWall.spawn_degrees(location=[-2.4 + x_offset, (-y*1.0)+2.55 + y_offset, 0.001], rotation=[0, 0, 0])

    for x in range (5):
        hWall.spawn_degrees(location=[-1.9+x + x_offset, 3.05+ y_offset, 0.001], rotation=[0, 0, 90])

    for y in range (6):
        hWall.spawn_degrees(location=[2.4+ x_offset, (-y*1.0)+2.55 + y_offset, 0.001], rotation=[0, 0, 0])

    for x in range (5):
        hWall.spawn_degrees(location=[-1.9+x+ x_offset, -3.05+ y_offset, 0.001], rotation=[0, 0, 90])

    hWall.spawn_degrees(location=[-2.03 + x_offset, -2.275+ y_offset, 0.001], rotation=[0, 0, 48])
    hWall.spawn_degrees(location=[-1.575+ x_offset, -2.7+ y_offset, 0.001], rotation=[0, 0, 48])


    # Spawn a QCar at the given initial pose
    car2 = QLabsQCar(qlabs)

    #-1.335+ x_offset, -2.5+ y_offset, 0.005
    #0, 0, -45
    car2.spawn_id(actorNumber=0, location=initialPosition, rotation=initialOrientation, scale=[.1, .1, .1], configuration=0, waitForConfirmation=True)
    basicshape2 = QLabsBasicShape(qlabs)
    basicshape2.spawn_id_and_parent_with_relative_transform(actorNumber=102, location=[1.15, 0, 1.8], rotation=[0, 0, 0], scale=[.65, .65, .1], configuration=basicshape2.SHAPE_SPHERE, parentClassID=car2.ID_QCAR, parentActorNumber=2, parentComponent=1,  waitForConfirmation=True)
    basicshape2.set_material_properties(color=[0.4,0,0], roughness=0.4, metallic=True, waitForConfirmation=True)

    camera1=QLabsFreeCamera(qlabs)
    camera1.spawn_degrees (location = [-0.426+ x_offset, -5.601+ y_offset, 4.823], rotation=[0, 41, 90])

    camera2=QLabsFreeCamera(qlabs)
    camera2.spawn_degrees (location = [-0.4+ x_offset, -4.562+ y_offset, 3.938], rotation=[0, 47, 90])

    camera3=QLabsFreeCamera(qlabs)
    camera3.spawn_degrees (location = [-0.36+ x_offset, -3.691+ y_offset, 2.652], rotation=[0, 47, 90])

    car2.possess()

    # stop signs
    myStopSign = QLabsStopSign(qlabs)
    myStopSign.spawn_degrees ([2.25 + x_offset, 1.5 + y_offset, 0.05], [0, 0, -90], [0.1, 0.1, 0.1], False)
    myStopSign.spawn_degrees ([-1.3 + x_offset, 2.9 + y_offset, 0.05], [0, 0, -15], [0.1, 0.1, 0.1], False)

    # Spawning crosswalks
    myCrossWalk = QLabsCrosswalk(qlabs)
    myCrossWalk.spawn_degrees (location =[-2 + x_offset, -1.475 + y_offset, 0.01],
                rotation=[0,0,0], scale = [0.1,0.1,0.075],
                configuration = 0)

    mySpline = QLabsBasicShape(qlabs)
    mySpline.spawn_degrees ([2.05 + x_offset, -1.5 + y_offset, 0.01], [0, 0, 0], [0.27, 0.02, 0.001], False)
    mySpline.spawn_degrees ([-2.075 + x_offset, y_offset, 0.01], [0, 0, 0], [0.27, 0.02, 0.001], False)
    car2.possess(car2.CAMERA_RGB)
    car2_image = car2.get_image(camera=car2.CAMERA_CSI_FRONT)
    lane_detection(car2_image[1], num)
    

    return car2


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    polygon = np.array([[(100, 407), (302, 212), (509, 212),(720, 407)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def lane_detection(image, num):
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(imageRGB)
    
    img.save("lane"+ num + ".png")
    cannyTransform = canny(image)
    cannyimg = Image.fromarray(cannyTransform)
    #cannyimg.save("lane"+ num + "canny" + ".png")

    
    


if __name__ == '__main__':
    car2 = main(initialPosition=[-1.959, 2.44, 0.0], initialOrientation=[0,0,-math.pi/2], num = "predict")
    
   
