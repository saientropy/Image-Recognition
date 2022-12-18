# -*- coding: utf-8 -*-
from collections import deque
import wiringpi as wp
import numpy as np
import imutils
import cv2
wp.wiringPiSetupGpio()
def Motor(x,y,pwm):
	wp.pinMode(x,1)
	wp.pinMode(y,1)
	wp.pinMode(pwm,1)
	wp.softPwmCreate(pwm,0,100)
	return x,y,pwm
motor1=Motor(27,17,4)
motor2=Motor(24,23,25)
def forward(motor1,motor2,speed1,speed2):
	(x,y,pwm)=motor1
	(a,b,pwm1)=motor2
	wp.digitalWrite(x,0)
	wp.digitalWrite(y,1)
	wp.softPwmWrite(pwm,speed1)
	wp.digitalWrite(a,0)
	wp.digitalWrite(b,1)
	wp.softPwmWrite(pwm1,speed2)
def clock(motor1,motor2,speed1,speed2):
	(x,y,pwm)=motor1
	(a,b,pwm1)=motor2
	wp.digitalWrite(x,1)
	wp.digitalWrite(y,0)
	wp.softPwmWrite(pwm,speed1)
	wp.digitalWrite(a,0)
	wp.digitalWrite(b,1)
	wp.softPwmWrite(pwm1,speed2)
def anticlock(motor1,motor2,speed1,speed2):
	(x,y,pwm)=motor1
	(a,b,pwm1)=motor2
	wp.digitalWrite(x,0)
	wp.digitalWrite(y,1)
	wp.softPwmWrite(pwm,speed1)
	wp.digitalWrite(a,1)
	wp.digitalWrite(b,0)
	wp.softPwmWrite(pwm1,speed2)
def stop(motor1,motor2):
	(x,y,pwm)=motor1
	(a,b,pwm1)=motor2
	wp.digitalWrite(x,0)
	wp.digitalWrite(y,0)
	wp.softPwmWrite(pwm,0)
	wp.digitalWrite(a,0)
	wp.digitalWrite(b,0)
	wp.softPwmWrite(pwm1,0)
x=0
y=0
r=0
HSV_Lower = (4,13,169)
HSV_Upper = (22,255,255)
camera = cv2.VideoCapture(0)
while True:
	ret, frame = camera.read()
	cv2.circle(frame,(325,215), 2, (0,255,0), -1)
	frame = imutils.resize(frame,width=600,height=400)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, HSV_Lower, HSV_Upper)
	cv2.imshow("mask",mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 0:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			x=int(x)
			y=int(y)
			r=int(radius)
			print x,y,r
	if r==0:
		stop(motor1,motor2)			
	if x>0 and x<250 and r<70:
		anticlock(motor1,motor2,20,20)
		#wp.delay(20)
	elif x>250 and x<450 and r<70:
		forward(motor1,motor2,20,20)
		#wp.delay(20)
	elif x>450 and x<600 and r<70:
		clock(motor1,motor2,20,20)
		#wp.delay(20)
	else:
		stop(motor1,motor2)
		#wp.delay(200)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
camera.release()
cv2.destroyAllWindows()
