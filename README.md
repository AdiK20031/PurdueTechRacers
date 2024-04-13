# Purdue Tech Racers

Welcome! This repository contains the files for the Purdue entry into the [Quanser Student Autonomous Car Competition](https://www.quanser.com/community/student-competition/2024-student-self-driving-car-competition/). This GitHub will serve as a common repostitory to store all our programs even if we utilize different computers, giving us one place to store our models and build a final solution. There will be 3 tasks for our team to accomplish.

- Obstacle detection
- Car control
- Lane control *staying in the proper lane*

Marked below is a checklist for the tasks these 3 teams will have to accomplish.


## Obstacle detection

- [ ] Generate training images in QCar (both from LIDAR and camera). 
- [ ] Label the training images.
- [ ] Creating a model and feeding these images into a model
- [ ] Create a loop to break car if obstacle is detected.

A script has been created to generate training images, simply run either stopsign.py or traffic_light.py and you will be able to commit pictures. Please make sure to pull the latest files from git using `git pull` before adding new images in order to not overwrite files.
## Car control

TBD

## Lane control

- [ ] Create code to turn car if lane is detected.

### NOTES

Please put comments in your code with your name and what your code does. 

[Documenation for QLabs and QCar](https://qlabs.quanserdocs.com/en/latest/) \
[Documentation for keras](https://keras.io/api/) \
https://thomasfermi.github.io/Algorithms-for-Automated-Driving/Introduction/intro.html \
https://github.com/Amin-Tgz/awesome-CARLA?tab=readme-ov-file \
https://www.labellerr.com/blog/real-time-lane-detection-for-self-driving-cars-using-opencv/ \
https://www.youtube.com/watch?v=eLTLtUVuuy4 \
https://www.youtube.com/watch?v=eLTLtUVuuy4 \

To pull from git\
`git pull` 

To commit to the git\
`git add *`\
`git commit -m "Commit message"`\
`git push origin main`

Please email the Team Capitan or Vice Team Capitan if you have any questions! 