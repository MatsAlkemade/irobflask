import numpy as np
import cv2
import os
import resultsToText as rtt
import databaseKoppeling as dbK
from datetime import datetime
import re


def matchTemplates():
    # img = cv2.resize(cv2.imread('assets/football_match.jpg', 0), (0, 0), fx=0.8, fy=0.8)
#     img = cv2.imread('assets/football_match.jpg')
    img = cv2.imread('Templates/new_Inv.jpg')
    # template = cv2.resize(cv2.imread('assets/football.png', 0), (0, 0), fx=0.8, fy=0.8)
    # h, w = template.shape

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    methods = [cv2.TM_CCOEFF_NORMED]

    folder_dir = "Templates3"
    templates = []
    filenames = []
    results = []
    cursor = 0
    for filename in os.listdir(folder_dir):
        template = cv2.imread(os.path.join(folder_dir, filename))
        if template is not None:
            templates.append(template)
            filenames.append(filename)

    for image in templates:
        template = image
        h = template.shape[0]
        w = template.shape[1]
        # print(h, w)
        cv2.imshow("image",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        for method in methods:
            img2 = img.copy()

            result = cv2.matchTemplate(img2, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                location = min_loc
                # print(1, min_val, "---", max_val)
            else:
                now = datetime.now()
                now = now.strftime("%d/%m/%Y %H:%M:%S")
                filename = re.sub("\D","",filenames[cursor])
                result = f"{round(max_val*100,2)}%,{filename},{now}"
                print("Match Value:",result)
                results.append(result)
                location = max_loc
                
#                 if max_val > 0.70:
#                     result = f"{round(max_val,2)}%, {filenames[cursor]}"
#                     print("Match Found! Value:",result)
#                     results.append(result)
# 
#                 else:
#                     print("No match found")
#                 location = max_loc

            cursor += 1
            bottom_right = (location[0] + w, location[1] + h)
            cv2.rectangle(img2, location, bottom_right, 255, 5)
            cv2.imshow('Match', img2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    rtt.writeToFile(results)
    rtt.textToCSV()
    dbK.koppelDB()
matchTemplates()