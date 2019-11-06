from pypylon import pylon
import cv2
import threading
import time



def thread_camera1():
    
    # connecting to the camera with specific IP
    ip_address = '192.168.2.110'
    info = pylon.DeviceInfo()
    info.SetPropertyValue('IpAddress', ip_address)
    camera1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera1.MaxNumBuffer = 10

    # Grabing Continusely (video) with minimal delay
    camera1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter_cam1 = pylon.ImageFormatConverter()

    # Set converter to converting grab-image data to opencv bgr format
    converter_cam1.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter_cam1.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    try:
        ### Grab image loop
        while camera1.IsGrabbing():
            # read grab image's result from camera whether it's sucessful or not.
            grabResult = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Success to grab image from GigE camera
            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter_cam1.Convert(grabResult)
                img = image.GetArray()
                cv2.imshow('Image from GigE camera1', img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            grabResult.Release()
            time.sleep(0.01)
            
    except Exception as e:
        print("task1 exception :\n")
        print(e)

    # Releasing the resource    
    camera1.StopGrabbing()
    cv2.destroyWindow('Image from GigE camera1')



def thread_camera2():
    # connecting to the camera with specific IP
    ip_address = '192.168.2.111'
    info = pylon.DeviceInfo()
    info.SetPropertyValue('IpAddress', ip_address)
    camera2 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera2.MaxNumBuffer = 10

    # Grabing Continusely (video) with minimal delay
    camera2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter_cam2 = pylon.ImageFormatConverter()

    # Set converter to converting grab-image data to opencv bgr format
    converter_cam2.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter_cam2.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
    try:
        ### Grab image loop
        while camera2.IsGrabbing():
            # read grab image's result from camera whether it's sucessful or not.
            grabResult = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Success to grab image from GigE camera
            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter_cam2.Convert(grabResult)
                img = image.GetArray()
                cv2.imshow('Image from GigE camera2', img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            grabResult.Release()
            time.sleep(0.01)
            
    except Exception as e:
        print("task2 exception :\n")
        print(e)

    # Releasing the resource    
    camera2.StopGrabbing()
    cv2.destroyWindow('Image from GigE camera2')



if __name__ == "__main__":
    lock = threading.Lock()
    t1 = threading.Thread(target=thread_camera1, args=())
    t2 = threading.Thread(target=thread_camera2, args=())
    t1.start()
    t2.start()