#from pypylon import pylon
#import urllib.request

import cv2
import numpy as np

#URL = "http://192.168.200.173:8080/video" #URL pour utiliser la camera du téléphone
capture  = cv2.VideoCapture(0)

def changeRes(frame,scale ):
   hauteur = int(frame.shape[1]*scale)
   largeur = int(frame.shape[0]*scale)
   dimensions = (hauteur,largeur)
   return cv2.resize ( frame, dimensions ,1 ,1 ,interpolation=cv2.INTER_AREA)

def empty(a):
    pass

cv2.namedWindow("Slider")
cv2.resizeWindow("Slider", 640,270)
cv2.createTrackbar("Hue Min","Slider",17,179,empty)
cv2.createTrackbar("Hue Max","Slider",77,179,empty)
cv2.createTrackbar("Sat Min","Slider",37,255,empty)
cv2.createTrackbar("Sat Max","Slider",255,255,empty)
cv2.createTrackbar("Val Min","Slider",4,255,empty)
cv2.createTrackbar("Val Max","Slider",255,255,empty)



while True:
    # Take each frame
    _, frame = capture.read()
    rezise = changeRes(frame,0.25)
    #canny = cv2.Canny(resize, 150, 200)
    
      
    H_min = cv2.getTrackbarPos("Hue Min", "Slider")
    H_max = cv2.getTrackbarPos("Hue Max", "Slider")
    S_min = cv2.getTrackbarPos("Sat Min", "Slider")
    S_max = cv2.getTrackbarPos("Sat Max", "Slider")
    V_min = cv2.getTrackbarPos("Val Min", "Slider")
    V_max = cv2.getTrackbarPos("Val Max", "Slider")
   
    
    lower = np.array([H_min,S_min,V_min])
    upper = np.array([H_max,S_max,V_max])
        
    hsv = cv2.cvtColor(rezise, cv2.COLOR_BGR2HSV)           
    mask = cv2.inRange(hsv, lower, upper)
       
    #removing noise
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
    segmented_img = cv2.bitwise_and(rezise, rezise, mask=mask)
    
    
        
    cv2.imshow('mask',mask)
    cv2.imshow('res',segmented_img)
    cv2.imshow('Telephone', rezise)
    cv2.imshow('hsv', hsv)
    
    #Pour terminer le prgrm
    q = cv2.waitKey(1)
    if q == ord("a"):
        break
        
capture.release()
cv2.destroyAllWindows()


"""
kernel = np.ones((5,5),np.uint8)

lower_Yellow = np.array([20, 80, 80])
upper_Yellow = np.array([30, 255, 255])

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_green = np.array([50, 20, 20])
upper_green = np.array([100, 255, 255])

lower_red = np.array([0, 100, 120])
upper_red = np.array([10, 255, 255])
"""




"""
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

new_width = camera.Width.GetValue() - camera.Width.GetInc()
if new_width >= camera.Width.GetMin():
    camera.Width.SetValue(new_width)

numberOfImagesToGrab = 100
camera.StartGrabbingMax(numberOfImagesToGrab)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        print("SizeX: ", grabResult.Width)
        print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        print("Gray value of first pixel: ", img[0, 0])

    grabResult.Release()
camera.Close()
"""
