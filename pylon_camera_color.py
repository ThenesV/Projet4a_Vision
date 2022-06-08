'''
https://github.com/basler/pypylon/issues/319
'''

import pypylon.pylon as pylon
import cv2
import numpy as np



try:

    # CONNECTER LA CAMERA AVEC LE NUMERO DE SERIE DE LA CAMERA
    info = pylon.DeviceInfo()
    info.SetSerialNumber('23265042')

    # CONNECTE LA CAMERA
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

    # MODELE DE LA CAMERA
    print ("Using Camera : ", camera.GetDeviceInfo().GetFriendlyName())

    # Open the camera to access features
    camera.Open()

    # PARAMETRES DE LA CAMERA
    camera.GetNodeMap().GetNode('Width').SetValue(640)
    camera.GetNodeMap().GetNode('Height').SetValue(480)

    # Driver/Grabber features are natively supported by the InstantCamera API
    # Because they are common to all camera interfaces
    camera.MaxNumBuffer.SetValue(20) # For demo only. Default is 10.

    # Start grabbing images.
    # NOMBRE d'images à enregistrer : StartGrabbingMax(numImages) 
    camera.StartGrabbingMax(4000) #Quand on atteint numImages, cela coupe la caméra

    while camera.IsGrabbing():

        # Retrieve a GrabResult from the driver
        result = camera.RetrieveResult(50000,pylon.TimeoutHandling_ThrowException)

        # The GrabResult is a container. It could hold a good image, corrupt image, no data, etc.
        if result.GrabSucceeded:
            
            # DEFINITION DE LA COULEUR DU MASQUE 
            #bleu
            lo_blue=np.array([95, 100, 50])
            hi_blue=np.array([105, 255, 255])
            color_infos=(0, 255, 255)    

            #rouge (à redéfinir)
            lo_red=np.array([0, 0, 50])
            hi_red=np.array([50, 50, 255])
            color_infos2=(255, 255, 0)  
            
         
            
            frame = result.GetArray()
            image=cv2.cvtColor(frame, cv2.cv2.COLOR_BGR2HSV)#COLOR_COLOR_BGR2HSV
            mask=cv2.inRange(image, lo_red, hi_red)#lo_blue, hi_blue
            image=cv2.blur(image, (7, 7))
            mask=cv2.erode(mask, None, iterations=4) 
            mask=cv2.dilate(mask, None, iterations=4)
            image2=cv2.bitwise_and(frame, frame, mask=mask)
            elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            # Detection de l'objet 
            if len(elements) > 0:
                c=max(elements, key=cv2.contourArea)
                ((x, y), rayon)=cv2.minEnclosingCircle(c)
                if rayon>30:
                    cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos2, 2)
                    cv2.circle(frame, (int(x), int(y)), 5, color_infos2, 10)
                    cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos2, 2)
                    cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos2, 1, cv2.LINE_AA)
                

            #Visuel sur la caméra, du masque avec le bleu, du masque bleu (en blanc)
            cv2.imshow('Camera', frame) #camera
            cv2.imshow('Camera filtre', image) #camera avec le filtre
            cv2.imshow('Camera2 filtre', image2) #camera avec le filtre en blanc


            cv2.waitKey(1)


        else:
            #ERREUR
            print ("")
            print ("Grab Result Failed!")
            print (" Error Description : ", result.GetErrorDescription())
            print (" Error Code        : ", result.GetErrorCode())

    print("")
    print( "finished!")

except pylon.GenericException as err:
    print("Pylon error: {0}".format(err))

