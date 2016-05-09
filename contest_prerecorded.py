#!/usr/bin/env python
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
import datetime
from gcloud import datastore

# create datastore client
client = datastore.Client("cafefritkotqueue")

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# setup webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


while True:
	# get image from webcam
	ret, image = cap.read()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# local logging
	with open("/home/jan/contest.log", "a") as f:
    		f.write(str(len(pick)))

	# put it in the cloud
	key = client.key("QueueLength")
	entry = datastore.Entity(key)
	entry.update({
		"Timestamp": datetime.datetime.utcnow(),
		"Length": len(pick)
	})
	client.put(entry)

cap.release()
logfile.close()
