'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler basler a640 100 gm (GigE, window 64bit , python 3.7)
'''
from pypylon import pylon
import cv2

# conecting to the first available camera
#camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# connecting to the camera with specific IP
ip_address = '192.168.2.110'
info = pylon.DeviceInfo()
info.SetPropertyValue('IpAddress', ip_address)
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned



### Grab image loop
while camera.IsGrabbing():
    # read grab image's result from camera whether it's sucessful or not.
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    # Success to grab image from GigE camera
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.imshow('from GigE camera', img)
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()



# Releasing the resource    
camera.StopGrabbing()

# Destroy all image windows
cv2.destroyAllWindows()