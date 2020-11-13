import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, default="",
	help="path to input image")
args = vars(ap.parse_args())

drawing = False # true if mouse is pressed # 
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
                cv2.circle(imAux,(x,y),thick,color,-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(imAux,(x,y),thick,color,-1)
cv2.namedWindow('imAux')
cv2.setMouseCallback('imAux',draw_circle)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

color_low = np.array([25, 52, 72], np.uint8)
color_up = np.array([50, 255, 255], np.uint8)

# Colors to paint
color_blue = (255,113,82)
color_yellow = (89,222,255)
color_pink = (128,0,255)
color_green = (0,255,36)
clear_screen = (29,112,246) # Will only be used for the upper box of 'Clean Screen'
# Line thickness upper left boxes (color to draw)
thickness_blue = 6
thickness_yellow = 2
thickness_pink = 2
thickness_green = 2

# Line thickness upper right boxes (thickness of the marker to draw)
small_thickness = 6
medium_thickness = 1
large_thickness = 1

# --------------------- Variables for the marker / virtual pen --------------------- ----
color = color_blue # Input color, and variable that will assign the marker color
thick = 3 # Thickness that the marker will have
#------------------------------------------------------------------------------------------

x1 = None
y1 = None

imAux = cv2.imread(args["image"]) # Reloading work
while True:

	ret,frame = cap.read()
	if ret==False: break

	frame = cv2.flip(frame,1)
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	if imAux is None: imAux = np.zeros(frame.shape,dtype=np.uint8)

    # ------------------------ Top Section ----------------------- -------------------
    # Squares drawn in the upper left (represent the color to be drawn)
	cv2.rectangle(frame,(0,0),(50,50),color_yellow,thickness_yellow)
	cv2.rectangle(frame,(50,0),(100,50),color_pink,thickness_pink)
	cv2.rectangle(frame,(100,0),(150,50),color_green,thickness_green)
	cv2.rectangle(frame,(150,0),(200,50),color_blue,thickness_blue)

    # Upper central rectangle, which will help us clean the screen
	cv2.rectangle(frame,(300,0),(400,50),clear_screen,1)
	cv2.putText(frame,'Clear',(320,20),6,0.6,clear_screen,1,cv2.LINE_AA)
	cv2.putText(frame,'Screen',(320,40),6,0.6,clear_screen,1,cv2.LINE_AA)

    # Squares drawn at the top right (marker thickness for drawing)
	cv2.rectangle(frame,(490,0),(540,50),(0,0,0),small_thickness)
	cv2.circle(frame,(515,25),3,(0,0,0),-1)
	cv2.rectangle(frame,(540,0),(590,50),(0,0,0),medium_thickness)
	cv2.circle(frame,(565,25),7,(0,0,0),-1)
	cv2.rectangle(frame,(590,0),(640,50),(0,0,0),large_thickness)
	cv2.circle(frame,(615,25),11,(0,0,0),-1)
	#-----------------------------------------------------------------------------------
	
    # Light blue color detection
	mask_out = cv2.inRange(frameHSV, color_low, color_up)
	mask_out = cv2.erode(mask_out,None,iterations = 1)
	mask_out = cv2.dilate(mask_out,None,iterations = 2)
	mask_out = cv2.medianBlur(mask_out, 13)
	cnts,_ = cv2.findContours(mask_out, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

	for c in cnts:
		area = cv2.contourArea(c)
		if area > 1000:
			x,y2,w,h = cv2.boundingRect(c)
			x2 = x + w//2
			
			if x1 is not None:
				if 0 < x2 < 50 and 0 < y2 < 50:
					color = color_yellow # Color of virtual pen / marker
					thickness_yellow = 6
					thickness_pink = 2
					thickness_green = 2
					thickness_blue = 2
				if 50 < x2 < 100 and 0 < y2 < 50:
					color = color_pink # Color of virtual pen / marker
					thickness_yellow = 2
					thickness_pink = 6
					thickness_green = 2
					thickness_blue = 2
				if 100 < x2 < 150 and 0 < y2 < 50:
					color = color_green # Color of virtual pen / marker
					thickness_yellow = 2
					thickness_pink = 2
					thickness_green = 6
					thickness_blue = 2
				if 150 < x2 < 200 and 0 < y2 < 50:
					color = color_blue # Color of virtual pen / marker
					thickness_yellow = 2
					thickness_pink = 2
					thickness_green = 2
					thickness_blue = 6
				if 490 < x2 < 540 and 0 < y2 < 50:
					thick = 3 # Thickness of virtual pen / marker
					small_thickness = 6
					medium_thickness = 1
					large_thickness = 1
				if 540 < x2 < 590 and 0 < y2 < 50:
					thick = 7 # Thickness of virtual pen / marker
					small_thickness = 1
					medium_thickness = 6
					large_thickness = 1
				if 590 < x2 < 640 and 0 < y2 < 50:
					thick = 11 # Thickness of virtual pen / marker
					small_thickness = 1
					medium_thickness = 1
					large_thickness = 6
				if 300 < x2 < 400 and 0 < y2 < 50:
					cv2.rectangle(frame,(300,0),(400,50),clear_screen,2)
					cv2.putText(frame,'Clear',(320,20),6,0.6,clear_screen,3,cv2.LINE_AA)
					cv2.putText(frame,'Screen',(320,40),6,0.6,clear_screen,3,cv2.LINE_AA)
					imAux = np.zeros(frame.shape,dtype=np.uint8)
				if 0 < y2 < 60 or 0 < y1 < 60 :
					imAux = imAux
				else:
					imAux = cv2.line(imAux,(x1,y1),(x2,y2),color,thick)
			cv2.circle(frame,(x2,y2),thick,color,3)
			x1 = x2
			y1 = y2
		else:
			x1, y1 = None, None
	
	imAuxGray = cv2.cvtColor(imAux,cv2.COLOR_BGR2GRAY)
	_, th = cv2.threshold(imAuxGray,10,255,cv2.THRESH_BINARY)
	thInv = cv2.bitwise_not(th)
	frame = cv2.bitwise_and(frame,frame,mask=thInv)
	frame = cv2.add(frame,imAux)
	
	
	cv2.imshow('imAux',imAux)  #drawing
	cv2.imshow('frame', frame) #input
	cv2.imshow('mask_out', mask_out) #countour
	
	k = cv2.waitKey(1)
	if k == 27 or k==113:   
		break  #exit
	if k == 115:
		cv2.imwrite("output.png",imAux) #saving image

cap.release()
cv2.destroyAllWindows()
