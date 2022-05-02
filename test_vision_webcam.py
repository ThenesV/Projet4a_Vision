#Show image, video, webcam

import cv2


#webcam
capture = cv2.VideoCapture(3) #0 default camera, 1

capture.set(3, 640) #width 3
capture.set(4, 480) #height 4
capture.set(10, 100) # 10 brightness

while True:
    success, img = capture.read() #save image in img, and tell if successful in success(true/False)
    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        #Stops if press q
        break
