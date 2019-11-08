'''
A simple Program for grabing video from basler camera and converting it to opencv img.
And then, Run Yolo object detection and display the result.

Tested on Basler basler a640 100 gm (GigE, window 64bit , python 3.7)
'''
from pypylon import pylon
import cv2
import numpy as np
import time


### Yolo section ###
# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# conecting to the first available camera
#camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# connecting to the camera with specific IP
ip_address = '192.168.3.110'
info = pylon.DeviceInfo()
info.SetPropertyValue('IpAddress', ip_address)
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

# Set Inter-Packet Delay in the Transport Layer to control bandwidth of camera. If not set it properly, It will fail to grab the image.
camera.Open()
camera.GevSCPD.SetValue(9000)   # Set Inter-Packet Delay (In tick)

# Grabing Continusely (video)
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
        yolo_img = np.copy(img)
        height, width, channels = yolo_img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(yolo_img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(yolo_img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(yolo_img, label, (x, y + 30), font, 3, color, 3)
        cv2.imshow("Yolo image", yolo_img)
        k = cv2.waitKey(1)
        if k == 27:
            break
        
    grabResult.Release()
    


# Releasing the resource    
camera.StopGrabbing()

# Destroy all image windows
cv2.destroyAllWindows()