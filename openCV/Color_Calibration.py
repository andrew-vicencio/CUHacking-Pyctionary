import numpy as np
import imutils
import cv2
from opencvFunc import *

windowName = "Colour Calibration"
lowerBound = [29, 86, 6]
upperBound = [64, 255, 255]
	
def trackbarEvent(foo):
	barNames = ["Hue Max", "Hue Min", "Sat Max", "Sat Min", "Value Max", "Value Min"]
	for i in range(6):
		if i % 2 == 0:
			upperBound[i/2] = cv2.getTrackbarPos(barNames[i], windowName)
		else:
			lowerBound[(i-1)/2] = cv2.getTrackbarPos(barNames[i], windowName)


cv2.namedWindow(windowName)
cv2.createTrackbar("Hue Max", windowName, 0, 180, trackbarEvent)
cv2.createTrackbar("Hue Min", windowName, 0, 180, trackbarEvent)
cv2.createTrackbar("Sat Max", windowName, 0, 255, trackbarEvent)
cv2.createTrackbar("Sat Min", windowName, 0, 255, trackbarEvent)
cv2.createTrackbar("Value Max", windowName, 0, 255, trackbarEvent)
cv2.createTrackbar("Value Min", windowName, 0, 255, trackbarEvent)

capture = cv2.VideoCapture(0)

while True:

	(captured, frame) = capture.read()

	mask = processFrame(frame, 640, tuple(upperBound), tuple(lowerBound))

	cv2.imshow(windowName, mask)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
 
capture.release()
cv2.destroyAllWindows()