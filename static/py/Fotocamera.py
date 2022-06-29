import cv2
import os.path
import os

def makePhoto():
    print("Camera Start")

    abs_path = "/var/www/irobflask/static/py"

    BG_path = f"{abs_path}/Status/BG.jpg"
    new_Inv_path = f"{abs_path}/Status/new_Inv.jpg"

    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(width, height)
    s, img = cam.read()
    img = cv2.flip(img,0)
    if s:    # frame captured without any errors
        #cv2.namedWindow("cam-test")
        #cv2.imshow("cam-test",img)
        #cv2.waitKey(0)
        #cv2.destroyWindow("cam-test")
        
        if os.path.exists(BG_path) and os.path.exists(new_Inv_path):
            # Background wordt de laatste nieuwe inventory
            new_BG = new_Inv_path# Dit wordt nieuwe background
            old_BG = BG_path
            os.rename(new_BG, old_BG)   #old file name, new file name
            print("Rename complete")
            
            # new inventory waarnemen
            cv2.imwrite(new_Inv_path,img) #save image
            
        
        elif not os.path.exists(BG_path):
            cv2.imwrite(BG_path,img) #save image
            print("background saved")
            
        elif os.path.exists(BG_path):
            new_inv = cv2.imwrite(new_Inv_path,img)
            print("new inventory saved")

# makePhoto()
            
