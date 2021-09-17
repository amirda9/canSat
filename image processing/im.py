import cv2,time
import numpy as np
def filterColor(image, lower, upper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return cv2.bitwise_and(image, image, mask= mask)

def moment(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray_image,0,200,cv2.THRESH_BINARY)
    M = cv2.moments(thresh)
    if M["m00"] !=0:
        return int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])
    else:
        return 0

cam = cv2.VideoCapture(0)
#it is for Green
upGreen = [90, 179, 150]
lowGreen = [70 , 80, 80]

upRed = [30, 255, 200]
lowRed = [0 , 150, 140]

upBlue = [127, 255, 255]
lowBlue = [100 , 127, 127]

while True:
    st = time.time()
    ret,image = cam.read()
    if ret:

        imageGreen = filterColor(image,lowGreen,upGreen)
        imageRed = filterColor(image,lowRed,upRed)
        imageBlue = filterColor(image,lowBlue,upBlue)

        x = moment(imageGreen)
        y = moment(imageRed)
        z = moment(imageBlue)
        

        if x:
            cv2.putText(image, "*", (x[0], x[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if y:
            cv2.putText(image, "*", (y[0], y[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        if z:
            cv2.putText(image, "*", (z[0], z[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('',image)
        cv2.waitKey(1)


    print(time.time()-st)
