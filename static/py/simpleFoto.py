import cv2
import os.path
import os

def makePhoto():
    print("Camera Start")

    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print(width, height)
    s, img = cam.read()
    if s:    # frame captured without any errors
        #cv2.namedWindow("cam-test")
        #cv2.imshow("cam-test",img)
        #cv2.waitKey(0)
        #cv2.destroyWindow("cam-test")

        cv2.imwrite("foto.jpg",img) #save image
        print("foto saved")




