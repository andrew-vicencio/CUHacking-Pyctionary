
import numpy as np
import cv2
import imutils

def processFrame(frame, windowWidth, upperBounds, lowerBounds):
	Wframe = imutils.resize(frame, width=windowWidth) # This is the visual output
	blurred = cv2.GaussianBlur(Wframe, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lowerBounds, upperBounds)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return mask

def findCenter(mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    radius = 0

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
    	c = max(cnts, key=cv2.contourArea)
    	((x, y), radius) = cv2.minEnclosingCircle(c)
    	M = cv2.moments(c)
    	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    return center, radius


def createMaze(windowHeight, windowWidth, mazeNumber):

	maze_image = np.zeros((windowHeight,windowWidth,3), np.uint8)

	# Create matrix for maze positions
	g = [[0 for y in range(6)] for x in range(8)]
	for x in range(8):
		for y in range(6):
   			g[x][y] = (x*windowWidth/8, y*windowHeight/6)

	lines = []
	start = []
	finish = []

	if mazeNumber == 0:
		lines.append([g[1][1],g[1][5],g[3][5],g[3][4],g[3][5],g[6][5],g[6][4],g[5][4],g[5][2],g[6][2],g[3][2]])
		lines.append([g[2][4],g[2][3],g[4][3],g[4][4]])
		lines.append([g[2][3],g[2][1],g[7][1],g[7][3],g[6][3],g[7][3],g[7][5]])
		start.append([g[1][1],g[2][1]])
		finish.append([g[6][5],g[7][5]])

	if mazeNumber == 1:
		lines.append([g[1][1], g[7][1], g[7][5], g[6][5]])
		lines.append([g[3][2], g[1][2], g[1][3], g[3][3], g[1][3], g[1][5], g[5][5], g[5][4], g[6][4], g[6][2], g[5][2], g[5][3]])
		lines.append([g[4][1], g[4][4], g[2][4]])
		start.append([g[1][1],g[1][2]])
		finish.append([g[5][5],g[6][5]])

	if mazeNumber == 2:
		lines.append([g[1][1], g[1][2], g[2][2], g[1][2], g[1][5], g[5][5], g[5][3], g[4][3], g[4][2]])
		lines.append([g[2][1], g[3][1], g[3][3], g[2][3], g[2][4], g[4][4]])
		lines.append([g[3][1], g[5][1], g[5][2], g[6][2], g[6][4]])
		lines.append([g[5][5], g[7][5], g[7][1], g[6][1]])
		start.append([g[1][1],g[2][1]])
		finish.append([g[5][1],g[6][1]])

	for l in range(len(lines)):
   		for i in range(len(lines[l])-1):
   			cv2.line(maze_image, lines[l][i], lines[l][i+1], (255, 255, 255), 10)
   	
   	cv2.line(maze_image, start[0][0], start[0][1], (255, 0, 0), 10)
   	cv2.line(maze_image, finish[0][0], finish[0][1], (255, 0, 0), 10)

   	templateContours = cv2.inRange(maze_image, (100,100,100), (255,255,255))
   	templateContours = cv2.findContours(templateContours,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2]

   	finishContours = cv2.inRange(maze_image, (85, 50, 40), (135, 255, 255))
   	finishContours = cv2.findContours(finishContours,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2]

	cv2.imwrite("maze.png", maze_image)

	return maze_image, templateContours, finishContours

def compareFrames(templateContours, frame, upperBounds, lowerBounds):

	frameTemplate = cv2.inRange(frame, lowerBounds, upperBounds)
	frameContours = cv2.findContours(frameTemplate,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[-2]
	diff = cv2.matchShapes(templateContours[0],frameContours[0],1,0.0)
	return diff

