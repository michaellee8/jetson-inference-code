import cv2
import imagezmq
image_hub = imagezmq.ImageHub(open_port='tcp://100.93.253.22:5555', REQ_REP=False)
image_hub.connect('tcp://100.93.253.22:5555')
window_name = "image"
font = cv2.FONT_HERSHEY_SIMPLEX
while True:  # show streamed images until Ctrl-C
    timestamp, image = image_hub.recv_image()
    cv2.putText(image, str(timestamp), (10,500), font, 1, (255,255,255), 2)
    print('received img at ', timestamp)
    cv2.imshow("image", image) # 1 window for each RPi

