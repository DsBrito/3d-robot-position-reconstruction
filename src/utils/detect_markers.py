import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

frame = cv2.imread("photo01.jpg")


img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
parameters =  aruco.DetectorParameters()
dictionary = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoDetector = aruco.ArucoDetector(dictionary, parameters)

corners, ids, rejectedImgPoints = arucoDetector.detectMarkers(img_rgb)
frame_markers = aruco.drawDetectedMarkers(img_rgb.copy(), corners, ids)

plt.figure()
plt.imshow(frame_markers, origin = "upper")
if ids is not None:
    for i in range(len(ids)):
        c = corners[i][0]
        plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "+", label = "id={0}".format(ids[i]))

plt.legend()
plt.show()
