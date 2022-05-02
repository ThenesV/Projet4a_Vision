'''
https://github.com/basler/pypylon/issues/319
'''

import os

os.environ["PYLON_CAMEMU"] = "3"

from pypylon import genicam
from pypylon import pylon
import sys
import cv2

converter = pylon.ImageFormatConverter()
# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#number max of camera
maxCamerasToUse = 1

# The exit code of the sample application.
exitCode = 0



try:

    # Get the transport layer factory.
    tlFactory = pylon.TlFactory.GetInstance()

    # Get all attached devices and exit application if no device is found.
    devices = tlFactory.EnumerateDevices()

    #NO CAMERA
    if len(devices) == 0:
        raise pylon.RuntimeException("No camera present.")

    # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
    cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse)) #return number of device, and the max of camera
    

    l = cameras.GetSize()

    # Create and attach all Pylon Devices.
    for i, cam in enumerate(cameras):
        cam.Attach(tlFactory.CreateDevice(devices[i])) #connect every camera

        # Print the model name of the camera.
        print("Using device ", cam.GetDeviceInfo().GetModelName())

    cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Grab c_countOfImagesToGrab from the cameras.
    

    #shows camera Image after connected succesfully
    while cameras.IsGrabbing():

        grabResult = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():

            cameraContextValue = grabResult.GetCameraContext()

            # Print the index and the model name of the camera.
            print("Camera ", cameraContextValue, ": ", cameras[cameraContextValue].GetDeviceInfo().GetModelName())

            # Now, the image data can be processed.
            #Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()

            window = 'Camera-{}'.format(cameraContextValue)
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.imshow(window, img)
            k = cv2.waitKey(1)
            if k == 27:
                print('break')            
                break



except genicam.GenericException as e:
    # Error handling
    print("An exception occurred.", e.GetDescription())
    exitCode = 1
