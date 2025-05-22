import cv2

def nothing():
	pass
	
title = "Trackbar test"

cv2.namedWindow(title)

cv2.createTrackbar('name1', title, 0, 255, nothing)

#Show some stuff
#on_trackbar(0)

#Wait until user press some key
cv2.waitKey()

