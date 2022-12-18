import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

GPIO.setmode(GPIO.BOARD)             # choose BCM or BOARD
GPIO.setup(21, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)# set GPIO24 as an output
GPIO.setwarnings(False)

def fwrd(t):
    GPIO.output(13,1)
    GPIO.output(21, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(13, 0)

def bkwrd(t):
    GPIO.output(23,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(23, 0)
    GPIO.output(15, 0)

def rght(t):
    GPIO.output(13,1)
    GPIO.output(23, 1)
    sleep(t)
    GPIO.output(13, 0)
    GPIO.output(23, 0)

def lft(t):
    GPIO.output(21,1)
    GPIO.output(15, 1)
    sleep(t)
    GPIO.output(21, 0)
    GPIO.output(15, 0)
ball_found == False
greenLower = (0,84,150)
greenUpper = (31, 255, 255)
def find_ball(ball_found):
	a,b,r=0,0,0
	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space, then initialize the
	# list of tracked points
	
	pts = deque(maxlen=args["buffer"])
	camera = cv2.VideoCapture(0)
	# keep looping
	while ball_found == False:
		# grab the current frame
		(grabbed, frame) = camera.read()

		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
		# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)t
		mask = cv2.dilate(mask, None, iterations=2)
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
			# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
				a,b,r=int(x),int(y),int(radius)
				print(a,b,r)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				ball_found == True
	turn_to_ball(a,b,r)
	
		
		
def turn_to_ball(x,y,r):
	global greenLower,greenUpper
	if( x > 320 and x<450):
		rght(0.05)
		while(r<200):
			fwrd(0.05)
		if 240>r>200:
			greenLower = (171,117,105)
			greenUpper = (182,255,255)
			find_ball(ball_found)
	elif( x < 300 and x>150):
		lft(0.05)
		while(r<200):
			fwrd(0.05)
		if 240>r>200:
			greenLower = (171,117,105)
			greenUpper = (182,255,255)
			find_ball(ball_found)
	elif(x>450):
		rght(0.08)
		while(r<200):
			fwrd(0.05)
		if 240>r>200:
			greenLower = (171,117,105)
			greenUpper = (182,255,255)
			find_ball(ball_found)
	else:
		lft(0.08)
		while(r<200):
			fwrd(0.05)
		if 240>r>200:
			greenLower = (171,117,105)
			greenUpper = (182,255,255)
			find_ball(ball_found)
	ball_found = True
	
def man():
	ball_found = False
	while(1):
		find_ball(ball_found)	
			