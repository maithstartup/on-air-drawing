# Overview 
You can draw on air, using an object of a specific color and we have set the default to green. This is achieved by using a few computer vision techniques which are implemented in OpenCV.

This program captures the user's video using their camera and sets up a drawing board using OpenCV. This contains a menu for colors, line thickness, and clearing the screen. The object to start drawing is detected and then used as the "marker" for the screen. In this specific case, the object detection is for a light blue object!

When the user wants to quit out of the program, the entire screen gets cleared and all windows become destroyed.

# Required Tools:
NumPy: used to perform math on arrays, matrices, etc. 

OpenCV: used for image processing and computer vision, using your camera module. It can be used for face detection, tracking, etc. In this case, it is used to draw!

# Installation 
- NumPy Installation:
  ```pip install numpy```
- OpenCV Installation:
  ```pip install opencv-python```

# Running the Program 
To run the program, run ```python draw.py``` in the CLI. 

# Demo 
[insert videos and pictures demoing how the actual program may work] 
