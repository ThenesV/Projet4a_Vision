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
    #camera.GetNodeMap().GetNode('Pixel Format').SetValue(BGR 8)


    # Driver/Grabber features are natively supported by the InstantCamera API
    # Because they are common to all camera interfaces
    camera.MaxNumBuffer.SetValue(20) # For demo only. Default is 10.

    # Start grabbing images.
    # NOMBRE d'images à enregistrer : StartGrabbingMax(numImages) 
    camera.StartGrabbingMax(10000) #Quand on atteint numImages, cela coupe la caméra

    def changeRes(frame,scale ):
        hauteur = int(frame.shape[1]*scale)
        largeur = int(frame.shape[0]*scale)
        dimensions = (hauteur,largeur)
        return cv2.resize ( frame, dimensions ,1 ,1 ,interpolation=cv2.INTER_AREA)

    def empty(a):
        pass


    #Creation d'une barre pour régler le masque en temps réel
    #valeur initiales bleu
    cv2.namedWindow("Slider")
    cv2.resizeWindow("Slider", 640,280)
    cv2.createTrackbar("Hue Min","Slider",95,179,empty)
    cv2.createTrackbar("Hue Max","Slider",105,179,empty)
    cv2.createTrackbar("Sat Min","Slider",100,255,empty)
    cv2.createTrackbar("Sat Max","Slider",255,255,empty)
    cv2.createTrackbar("Val Min","Slider",50,255,empty)
    cv2.createTrackbar("Val Max","Slider",255,255,empty)

    lower = np.array([95,100,50])
    upper = np.array([105,255,255])

    test = 0

    while camera.IsGrabbing():

        # Retrieve a GrabResult from the driver
        result = camera.RetrieveResult(50000,pylon.TimeoutHandling_ThrowException)

        # The GrabResult is a container. It could hold a good image, corrupt image, no data, etc.
        if result.GrabSucceeded:
            test +=1

            # DEFINITION DE LA COULEUR DU MASQUE 
            '''
            #bleu
            lo_blue=np.array([95, 100, 50])
            hi_blue=np.array([105, 255, 255])
            color_infos=(0, 255, 255)    

            #rouge
            lo_red=np.array([0, 0, 50])
            hi_red=np.array([50, 50, 255])
            color_infos2=(255, 255, 0)  '''

            frame = result.GetArray()

            rezise = changeRes(frame,1)
            rezise2 = changeRes(frame,1)

            # Slider - barre pour modifier les valeurs HSV
            
            H_min = cv2.getTrackbarPos("Hue Min", "Slider")
            H_max = cv2.getTrackbarPos("Hue Max", "Slider")
            S_min = cv2.getTrackbarPos("Sat Min", "Slider")
            S_max = cv2.getTrackbarPos("Sat Max", "Slider")
            V_min = cv2.getTrackbarPos("Val Min", "Slider")
            V_max = cv2.getTrackbarPos("Val Max", "Slider")


            #Mask initialement bleu
            lower = np.array([H_min,S_min,V_min])
            upper = np.array([H_max,S_max,V_max])
               
            hsv = cv2.cvtColor(rezise, cv2.COLOR_BGR2HSV)           
            mask = cv2.inRange(hsv, lower, upper)

            color_infos = (255, 255, 255) 
            image2=cv2.bitwise_and(frame, frame, mask=mask)
            elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            # Detection de l'objet 
            if len(elements) > 0:
                c=max(elements, key=cv2.contourArea)
                ((x, y), rayon)=cv2.minEnclosingCircle(c)
                if rayon>30:
                    cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos, 2)
                    cv2.circle(frame, (int(x), int(y)), 5, color_infos, 10)
                    cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos, 2)
                    cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
       
            segmented_img = cv2.bitwise_and(rezise, rezise, mask=mask)

            #Visuel sur la caméra, du masque avec le bleu, du masque bleu (en blanc)
            cv2.imshow('Camera', frame) #camera
            cv2.imshow('Camera filtre', mask) #camera avec le filtre
            cv2.imshow('Camera2 filtre', segmented_img) #camera avec le filtre en blanc

            

            #condition pour quchecker seulement sur la premiere image
            if test<2:

                #taille de l'image (bleu)
                long_image = np.shape(segmented_img)[0]#lignes
                larg_image = np.shape(segmented_img)[1]#colonnes

                #print('long',long_image, 'larg',larg_image)

                compteur_bleu_gauche = 0
                compteur_bleu_droite = 0

                compteur_rouge_gauche = 0
                compteur_rouge_droite = 0

                '''
                Image

                    
                -------------
                |            |
                | X          | 
                | X          |
                -------------

                X = couleur bleu
                Si X coté gauche de l'image, on compte les pixels bleu coté gauche puis coté droit de l'image => compare => coté gauche => robot doit aller côté gauche

                '''



                '''COTE POUR LA COULEUR BLEU'''
                #Compte les pixels bleu coté gauche de l'image
                for i in range(int(larg_image/2)):
                    for j in range(long_image):  
                        if segmented_img[j][i][1]!=0:
                            compteur_bleu_gauche +=1

                #Compte les pixels bleu coté droit de l'image
                for i in range(int(larg_image/2), larg_image):
                    for j in range(long_image):
                        if segmented_img[j][i][1]!=0:
                            compteur_bleu_droite +=1

                print ('Nombre pixels bleu côté')
                print('Gauche',compteur_bleu_gauche,'Droit', compteur_bleu_droite)

                #compare le nombre de pixels pour connaitre la position de l'objet => gauche ou droit
                if compteur_bleu_gauche > compteur_bleu_droite:
                    donnee = [1,0] #information à envoyer au robot
                    print('L Objet est cote gauche')

                else :
                    donnee = [0,1]
                    print('L Objet est cote droit')

                


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
