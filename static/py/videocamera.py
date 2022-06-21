import cv2
import numpy as np

def video_on():

    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:

    #     print(width, height)

        s, img = cam.read()
        image = np.zeros(img.shape,np.uint8)
        img = cv2.flip(img,0)
        cv2.imshow('frame',img)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
    cam.release()
    cv2.destroyWindow("cam-test")
    #cv2.imwrite("AAAFOTO.jpg",img) #save image

video_on()
