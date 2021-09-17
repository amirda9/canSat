import cv2
import numpy as np

class getLocationByCamera:
    Robots = 3
    cam = 0
    cam_port = 0


    filter = {'upGreen' : [90, 179, 150],\
            'lowGreen' : [70 , 80, 80],\
            'upBlue' : [127, 255, 255],\
            'lowBlue' : [100 , 127, 127],\
            'upRed' : [30, 255, 200],\
            'lowRed' : [0 , 150, 140],}

    errorLib = {'filter': 'not enough filters available for the number of Robots\
                 you entered\n the default is 3!',\
                'camera': 'no camera is found!',\
                'image': 'error in camera:\n camera might not detected or does not respond'}
    
    def __init__(self,Robots = None):
        if Robots is not None:
            if ((len(self.filter)/2) != Robots):
                print(self.errorLib('filter'))
            else:   
                self.Robots = Robots
                self.filter = list(self.filter.values())  
        try:
            self.cam = cv2.VideoCapture(self.cam_port)
        except:
            try:
                self.cam = cv2.VideoCapture(int(not self.cam_port))
            except:
                print(self.errorLib['camera'])


    def __del__(self):
        try:
            self.cam.release()
        except:
            self.cam = 0

    #filter color based on hsv lower and upper argument given
    def filterColor(self,image, lower, upper):      
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        return cv2.bitwise_and(image, image, mask= mask)

    #find the center of mass of a given image
    def moment(self,image):     
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray_image,0,200,0)
        M = cv2.moments(thresh)
        if M["m00"] !=0:
            return int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])
        else:
            return [-1,-1]
    
    def getLocationFromImage(self):
        ret,image = self.cam.read()
        robotLoc = []
        if ret:
            for i in range(self.Robots):  
                robotLoc.append(self.moment(self.filterColor(image,self.filter[2*i+1],self.filter[2*i])))
            return robotLoc[0][0],robotLoc[1][0],robotLoc[2][0],\
                   robotLoc[0][1],robotLoc[1][1],robotLoc[2][1]
        else:
            print(self.errorLib['image'])
            return 0

        




            
