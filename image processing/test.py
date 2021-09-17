from PIL import Image
import cv2
import numpy as np

image = Image.open("test.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, np.array(100), np.array(200))
img = cv2.bitwise_and(image, image, mask= mask)