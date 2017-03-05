
from collections import deque
import numpy as np
import imutils
import cv2
from opencvFunc import *

orangeLower = (0, 120, 178)
orangeUpper= (20, 255, 255)
greenLower = (50, 100, 100)
greenUpper = (70, 255, 255)
whiteUpper = (0,0,255)
whiteLower = (0,0,100)

windowHeight = 480
windowWidth = 640
numberOfPoints = 32
pts = deque(maxlen=numberOfPoints)  # Deque containing last 32 point history
counter = 0  # Frame counter
(dX, dY) = (0, 0)  # Velocity of movement in x,y directions
direction = ""
touchedWall = False
 
capture = cv2.VideoCapture(0)  # Create camera capture object
# Blank image for drawing shapes
mazeImage = createMaze(windowHeight, windowWidth)

template = cv2.imread("maze.png", 0)
templateContours = cv2.findContours(template,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2]
# Blank image for drawing shapes

while True:
    # get the current frame
    (captured, frame) = capture.read()
    frame = cv2.flip(frame, 1)
    
    # Image manipulations to draw out single colour
    mask = processFrame(frame, windowWidth, orangeUpper, orangeLower)
    
    # Test if pointer crossed wall of maze
    # Expensive so only run every 10th frame
    if counter % 10 == 0:
        dynamicTemplate = cv2.inRange(mazeImage, (100,100,100), (255,255,255))
        dynContours = cv2.findContours(dynamicTemplate,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2]
        ret = cv2.matchShapes(templateContours[0],dynContours[0],1,0.0)
        if(ret != 0):
            print("You hit the wall!")
            touchedWall = True
            break
 
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    circle = findCenter(mask)
    center = circle[0]
    radius = circle[1]
 
        # only proceed if the radius meets a minimum size
    if radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, center, int(radius), (0, 0, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        pts.appendleft(center)  # Append x,y coords of center

            # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them

        if pts[i - 1] is None or pts[i] is None:
            continue
 
        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 10 and i == 1 and len(pts) > 15:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[0][0] - pts[15][0]
            dY = pts[0][1] - pts[15][1]
            

        # Old lines get overidden since buffer only contains last 32 points
        cv2.line(mazeImage, pts[i - 1], pts[i], (0, 255, 0), 10)
 
 
    # show the frame to the screen and increment the frame counter
    cv2.imshow("Pyctionary", frame)
    cv2.imshow("Drawing", mazeImage)

    key = cv2.waitKey(1) & 0xFF
    counter += 1
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
capture.release()
cv2.destroyAllWindows()