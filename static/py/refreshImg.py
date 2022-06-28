import cv2
import os.path
import os

def refreshImg():
    img_path = "/var/www/irobflask/static/img/fridge.jpeg"

    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    s, img = cam.read()

    if s:    # frame captured without any errors
        if os.path.exists(img_path):
            cv2.imwrite(img_path,img) #save image
            print("Success")
            return "Success"

        else:
            print("Failed at path")
            return "Failed at path"

    else:
        print("Failed at s")
        return "Failed at s"

# refreshImg()