import pypylon.pylon as pylon
import cv2

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
    # The camera's physical acquisition starts, and the driver's streamgrabber is configured (buffers created, etc.)
    # StartGrabbingMax(numImages) will call StopGrabbing() automatically when numImages are retrieved.
    camera.StartGrabbingMax(5000)

    while camera.IsGrabbing():

        # Retrieve a GrabResult from the driver
        result = camera.RetrieveResult(5000,pylon.TimeoutHandling_ThrowException)

        # The GrabResult is a container. It could hold a good image, corrupt image, no data, etc.
        if result.GrabSucceeded:
            print("")
            print ("Grab Result Succeeded! We have an Image!")
            print (" Image number              : ", result.GetBlockID())
            print (" Dimensions                : ", result.GetWidth(), "x", result.GetHeight())
            buffer = result.GetBuffer()
            print (" Gray value of first pixel : ", buffer[0])
            
            # Display using OpenCV (optional for this example)
            # imshow supports only 1,3,4 bytes/pixel. YUV is 2. So we convert to BGR
            if pylon.IsYUV(result.GetPixelType()):
                myImage = cv2.cvtColor(result.GetArray(), cv2.COLOR_YUV2BGR_YUYV )
            else:
                myImage = result.GetArray() # GetArray() returns a numpy array suitable for OpenCV
                
            cv2.imshow('', myImage)
            cv2.waitKey(1)

        else:
            print ("")
            print ("Grab Result Failed!")
            print (" Error Description : ", result.GetErrorDescription())
            print (" Error Code        : ", result.GetErrorCode())

    print ("")
    print ("finished!")

except pylon.GenericException as err:
    print("Pylon error: {0}".format(err))