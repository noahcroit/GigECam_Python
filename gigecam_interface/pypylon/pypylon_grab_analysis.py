# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam

import sys
import time

# Number of sample images to be grabbed.
countOfImagesToGrab = int(input("Enter the number of sample image for grab analysis\n: "))


# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device with specific IP address
    ip_address = '192.168.3.110'
    info = pylon.DeviceInfo()
    info.SetPropertyValue('IpAddress', ip_address)
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
    camera.Open()

    # Set packet-delay in transport layer
    camera.GevSCPD.SetValue(7000)
    print(camera.GevSCPD.GetValue())

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # demonstrate some feature access
    new_width = camera.Width.GetValue() - camera.Width.GetInc()
    if new_width >= camera.Width.GetMin():
        camera.Width.SetValue(new_width)

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer = 5

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfImagesToGrab)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    grab_success_cnt = 0
    grab_fail_cnt = 0
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():
            grab_success_cnt += 1
            """
            # Access the image data.
            print("SizeX: ", grabResult.Width)
            print("SizeY: ", grabResult.Height)
            img = grabResult.Array
            print("Gray value of first pixel: ", img[0, 0])
            """
        else:
            grab_fail_cnt += 1
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)

        grabResult.Release()

    camera.Close()

    # Display grabbing result
    print("Success : {},\tFailed : {}".format(grab_success_cnt, grab_fail_cnt))

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)