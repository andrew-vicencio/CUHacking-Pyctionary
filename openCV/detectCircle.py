
from collections import deque
import numpy as np
import imutils
import cv2, os
import os.path

if os.path.exists('fifo'):
    os.remove('fifo')
os.mkfifo('fifo')
fifo = open('fifo', 'w');

redUpper = (0, 0, 0)
redUpper = (0, 0, 0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
redUpper = (0, 0, 0)
redUpper = (0, 0, 0)

numberOfPoints = 32
pts = deque(maxlen=numberOfPoints)  # Deque containing last 32 point history
counter = 0  # Frame counter
(dX, dY) = (0, 0)  # Velocity of movement in x,y directions
direction = ""
 
capture = cv2.VideoCapture(0)  # Create camera capture object


while True:
    # get the current frame
    (captured, frame) = capture.read()
    
    # Image manipulations to draw out single colour
    frame = imutils.resize(frame, width=900) # This is the visual output
    frame = cv2.flip(frame,1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
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
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)  # Append x,y coords of center
            fifo.write("{}:{}\n".format(pts[0][0], pts[0][1]))
            fifo.flush();


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
            (dirX, dirY) = ("", "")
 
            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"
 
            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"
 
            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)
 
            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY
            
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(numberOfPoints / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
    # show the movement deltas and the direction of movement on
    # the frame
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)
 
    # show the frame to our screen and increment the frame counter
    cv2.imshow("Pyctionary", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
capture.release()
cv2.destroyAllWindows()
fifo.close()
os.remove("fifo")
