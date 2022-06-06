'''
https://github.com/basler/pypylon/issues/319
'''

import pypylon.pylon as pylon
import cv2
import numpy as np

lo=np.array([95, 100, 50])
hi=np.array([105, 255, 255])
color_infos=(0, 255, 255)

try:

    # We can optionally define a Device Info Object to use in finding a specific camera
    info = pylon.DeviceInfo()
    info.SetSerialNumber('23265042')

    # The InstantCamera is generic (interface agnostic)
    # It encapsulates the physical camera and driver into one convinient object
    # Open the first camera found that matches the Device Info Object (optional)
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

    print ("Using Camera : ", camera.GetDeviceInfo().GetFriendlyName())

    # Open the camera to access features
    camera.Open()

    # We use the Genicam API to change features via strings
    # because we are programming generically
    camera.GetNodeMap().GetNode('Width').SetValue(640)
    camera.GetNodeMap().GetNode('Height').SetValue(480)

    # Driver/Grabber features are natively supported by the InstantCamera API
    # Because they are common to all camera interfaces
    camera.MaxNumBuffer.SetValue(20) # For demo only. Default is 10.

    # Start grabbing images.
    # StartGrabbingMax(numImages) will call StopGrabbing() automatically when numImages are retrieved.
    camera.StartGrabbingMax(4000)

    while camera.IsGrabbing():

        # Retrieve a GrabResult from the driver
        result = camera.RetrieveResult(50000,pylon.TimeoutHandling_ThrowException)

        # The GrabResult is a container. It could hold a good image, corrupt image, no data, etc.
        if result.GrabSucceeded:
            '''
            print ("")
            print ("Grab Result Succeeded! We have an Image!")
            print (" Image number              : ", result.GetBlockID())
            print (" Dimensions                : ", result.GetWidth(), "x", result.GetHeight())
            buffer = result.GetBuffer()
            print (" Gray value of first pixel : ", buffer[0])'''
            '''
            # Display using OpenCV (optional for this example)
            # imshow supports only 1,3,4 bytes/pixel. YUV is 2. So we convert to BGR
            if pylon.IsYUV(result.GetPixelType()):
                #myImage = cv2.cvtColor(result.GetArray(), cv2.COLOR_YUV2BGR_YUYV )
                DEFINE cv2 COLOR
                #myImage = cv2.cvtColor(result.GetArray(), cv2.COLOR_BGR2GRAY)

                frame = result.GetArray()

                print("if")
                
                mask1 = cv2.inRange(image, (36, 0, 0), (70, 255,255))
                mask2 = cv2.inRange(image, (15,0,0), (36, 255, 255))

                mask = cv2.bitwise_or(mask1, mask2)
                target = cv2.bitwise_and(image,image, mask=mask)
                image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                '''
                
         
            
            
            frame = result.GetArray()
            #cam = result.GetArray()
            
            
            print("else")
            image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask=cv2.inRange(image, lo, hi)
            image=cv2.blur(image, (7, 7))
            mask=cv2.erode(mask, None, iterations=4)
            mask=cv2.dilate(mask, None, iterations=4)
            image2=cv2.bitwise_and(frame, frame, mask=mask)
            elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            if len(elements) > 0:
                c=max(elements, key=cv2.contourArea)
                ((x, y), rayon)=cv2.minEnclosingCircle(c)
                if rayon>30:
                    cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos, 2)
                    cv2.circle(frame, (int(x), int(y)), 5, color_infos, 10)
                    cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos, 2)
                    cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
                
            
            cv2.imshow('Camera', image) #show camera



            cv2.waitKey(1)

            '''
            import numpy as np

            lo=np.array([95, 100, 50])
            hi=np.array([105, 255, 255])
            color_infos=(0, 255, 255)
            cap=cv2.VideoCapture(0)

            while True:
                ret, frame=cap.read()
                image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask=cv2.inRange(image, lo, hi)
                image=cv2.blur(image, (7, 7))
                mask=cv2.erode(mask, None, iterations=4)
                mask=cv2.dilate(mask, None, iterations=4)
                image2=cv2.bitwise_and(frame, frame, mask=mask)
                elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                if len(elements) > 0:
                    c=max(elements, key=cv2.contourArea)
                    ((x, y), rayon)=cv2.minEnclosingCircle(c)
                    if rayon>30:
                        cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos, 2)
                        cv2.circle(frame, (int(x), int(y)), 5, color_infos, 10)
                        cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos, 2)
                        cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
                cv2.imshow('Camera', frame) #show camera
                cv2.imshow('image2', image2) #show camera (only blue color)
                cv2.imshow('Mask', mask) #show blue color in white
                if cv2.waitKey(1)&0xFF==ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            '''

        else:
            print ("")
            print ("Grab Result Failed!")
            print (" Error Description : ", result.GetErrorDescription())
            print (" Error Code        : ", result.GetErrorCode())

    print("")
    print( "finished!")

except pylon.GenericException as err:
    print("Pylon error: {0}".format(err))

