# Automatically
# While door == closed
# Take photo
# Controleer of QR code is
# if QR code == True: stay in loop
# Else door == opened
# Als door == opened verandert naar deur is closed
# makePhoto(), matchTemplate

import simpleFoto as sf
import TemplateMatcher
import Fotocamera as fc
import TemplateMatching_IMG_folder as match
import videocamera as videocam

from time import sleep
door_closed = True
# QR_code = False

while True:
    # print("Take Photo")
    sf.makePhoto()
    QR_code = TemplateMatcher.matchTemplates()
    print(QR_code)

    if QR_code == False:
        print("QR = False, Door is open")
        sleep(20) # wacht 20 seconden tot dat waarschijnlijk de koelkast dicht is
        sf.makePhoto()
        QR_code = TemplateMatcher.matchTemplates()

        if QR_code == False:
            print("yaye")
            continue

        elif QR_code == True:    # moet in werkelijkheid True zijn
            print("QR = True, Door is closed")
            door_closed = True
            fc.makePhoto()
            match.matchTemplates()
            continue

    elif QR_code == True:
        sleep(2)
        continue




