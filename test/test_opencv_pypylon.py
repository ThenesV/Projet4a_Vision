'''from pypylon import pylon 
from pypylon_opencv_viewer import BaslerOpenCVViewer
import cv2
import numpy as np

# Pypylon get camera by serial number
serial_number = '23265042'
info = None
for i in pylon.TlFactory.GetInstance().EnumerateDevices():
    if i.GetSerialNumber() == serial_number:
        info = i
        break
else:
    print('Camera with {} serial number not found'.format(serial_number))

# VERY IMPORTANT STEP! To use Basler PyPylon OpenCV viewer you have to call .Open() method on you camera
if info is not None:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(info))
    camera.Open()

viewer = BaslerOpenCVViewer(camera)

def impro(img):
   return np.hstack([img, (255-img)])
viewer.set_impro_function(impro)

def impro(img):
    cv2.namedWindow('1', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('1', 1080, 720)
    cv2.imshow("1", np.hstack([img, (255-img)]))
viewer.set_impro_function(impro, own_window=True)

def impro(img):
    img_rgb = img.copy()
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    _, img_gray = cv2.threshold(img_gray, 170, 255, cv2.THRESH_BINARY)
    img_gray = 255 - img_gray
    _, contours, _ = cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    selected_contours = []
    for c in contours:
        contour_area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)        
        bounding_rect_area = w*h
        if(contour_area > 80 and contour_area/bounding_rect_area < 0.75):
            selected_contours.append(c)

    cv2.drawContours(img_rgb, selected_contours, -1, (0,0,255), thickness=cv2.FILLED)    
    img = cv2.putText(img, "Original", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,0,0), 8)
    img_rgb = cv2.putText(img_rgb, "Found numbers", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,0,0), 8)
    return np.hstack([img, img_rgb])

# Save image
viewer.save_image('~/Documents/images/grabbed.png')

# Get grabbed image
img = viewer.get_image()
'''


'''
from pypylon import pylon
import cv2

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

cv2.destroyAllWindows()
'''

import cv2
import pypylon.pylon as py
icam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())

icam.Open()
icam.PixelFormat = "RGB8"

img = icam.GrabOne(4000)

img = img.Array
cv2.cvtColor(img, cv2.COLOR_RGB2BGR)