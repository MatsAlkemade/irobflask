import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import cv2
import os
import os.path

def makeTemplate():
#     im1 = mpimg.imread('assets/BBB.jpg')
#     bg1 = mpimg.imread('assets/AAA.jpg')
    im1 = mpimg.imread('Templates/new_Inv.jpg')
    bg1 = mpimg.imread('Templates/BG.jpg')

    #test = mpimg.imread('assets/koelkast2.jpeg')
    # test = mpimg.imread('assets/bb_test4.jpeg')

    #Background IMG

    #Last Image


    scale_percent = 100  # percent of original size
    width_im1 = int(im1.shape[1] * scale_percent / 100)
    height_im1 = int(im1.shape[0] * scale_percent / 100)
    dim_im1 = (width_im1, height_im1)

    width_bg1 = int(bg1.shape[1] * scale_percent / 100)
    height_bg1 = int(bg1.shape[0] * scale_percent / 100)
    dim_bg1 = (width_bg1, height_bg1)

    # resize image
    resized_im1 = cv2.resize(im1, dim_im1, interpolation=cv2.INTER_AREA)
    resized_bg1 = cv2.resize(bg1, dim_bg1, interpolation=cv2.INTER_AREA)

    im1 = resized_im1
    bg1 = resized_bg1

    #Over de ingeladen afbeeldingen gooi ik een blur filter. Dit zorgt ervoor dat 0 waarden (hopelijk)
    #op niet-0 worden gezet. Het verwijdert wat details. 0 waarden leveren problemen op bij de cosinus.

    kernel = np.ones((3,3),np.float32)/9
    im1 = cv2.filter2D(im1,-1,kernel)
    bg1 = cv2.filter2D(bg1,-1,kernel)

    # EVEN weg gezet
#     plt.imshow(im1)
#     plt.show()
#     plt.imshow(bg1)
#     plt.show()

    #Hier een simpele check wat de dimensies zijn van de afbeelding. In dit geval 240 bij 320 pixel. De 3 is van de kleur rgb
    #print(im1.shape)

    #Hier controleer ik of er geen 0 waarden in de afbeelding zitten.
    #print(np.min(im1))

    # ZO KAN JE ZIEN WELKE KLEUREN DOMINANT ZIJN
    # kanaal = 0
    # plt.imshow(im1[:,:,kanaal],cmap='gray')
    # plt.show()

    #Een afbeelding kun je afvlakken en dan een histogram plotten. Zo kun je pieken detecteren die met
    #het verschil zijn in de twee afbeeldingen.

    # HISTOGRAMMEN DIE GEBRUIKT KUNNEN WORDEN VOOR HERKENNING
    # plt.hist(im1[:,:,0].flatten(),bins=50)
    # plt.show()
    # plt.hist(bg1[:,:,0].flatten(),bins=50)
    # plt.show()

    #Hier gaan we vectormeetkunde gebruiken om de achtegrond van de voorgrond te filteren.
    # We gebruiken als eerste de afstand tussen twee vectoren.
    # Dit is de stelling van Pythagoras. De int16 wordt gebruikt om negatieve getallen toe te laten.
    # Delen door 255 is voor de normalisatie.

    red   = (bg1[:,:,0].astype('int16')/255-im1[:,:,0].astype('int16')/255)**2
    green = (bg1[:,:,1].astype('int16')/255-im1[:,:,1].astype('int16')/255)**2
    blue  = (bg1[:,:,2].astype('int16')/255-im1[:,:,2].astype('int16')/255)**2
    diff = np.sqrt(red+green+blue)
    # diff is de afstand tussen twee vectoren. Dit gebeurt voor alle pixels in de afbeelding.

    #Hier gaan we de lengte berekenen van de vectoren. We doen dit voor de achtegrond en voorgrond.

    red   = (bg1[:,:,0].astype('int16')/255)**2
    green = (bg1[:,:,1].astype('int16')/255)**2
    blue  = (bg1[:,:,2].astype('int16')/255)**2
    lenbg1 = np.sqrt(red+green+blue)

    red   = (im1[:,:,0].astype('int16')/255)**2
    green = (im1[:,:,1].astype('int16')/255)**2
    blue  = (im1[:,:,2].astype('int16')/255)**2
    lenim1 = np.sqrt(red+green+blue)

    # We berekenen het inwendig product tussen de vectoren. Hiermee berekenen we de hoek cosinus-a
    dot0 = bg1[:,:,0].astype('int16')/255*im1[:,:,0].astype('int16')/255
    dot1 = bg1[:,:,1].astype('int16')/255*im1[:,:,1].astype('int16')/255
    dot2 = bg1[:,:,2].astype('int16')/255*im1[:,:,2].astype('int16')/255

    # De hoek cosinusa-a
    angle = (dot0+dot1+dot2)/((lenbg1)*(lenim1))

    #Nu we de afstand hebben en de cosinus-a kunnen we gaan spelen met een threshold waarde om de object uit te snijden.
    # We beginnen bij de afstand. We kijken naar het histogram om een threshold waarde te bepalen.

    th1 = diff>0.25 #Filter/threshold

    # HISTOGRAM DAT NODIG IS OM THRESHOLD WAARDE TE BEPALEN
    # plt.hist(diff.flatten(),bins=100)
    # plt.show()

    # Gebruik de threshold waarde om alle waarden die niet over de threshold heenkomen op 0 te zetten.
    dummy = np.copy(im1)
    dummy[:,:,0] = dummy[:,:,0]*th1
    dummy[:,:,1] = dummy[:,:,1]*th1
    dummy[:,:,2] = dummy[:,:,2]*th1

    #Nu kunnen we het resultaat zien van het uitsnijden van objecten.
#     plt.imshow(dummy)
#     plt.show()

    # Voor de hoek ga ik de hoek resultaten nog blurren voor een beter resultaat.
    smooth = np.ones((3,3),np.float32)/9
    dst = cv2.filter2D(angle,-1,smooth)

    #We plotten een histogram om te kijken waar we de treshold moeten leggen. De waarden liggen heel hoog tegen 1 aan.
    # plt.hist(angle.flatten(),bins=100)
    # plt.show()
    # plt.hist(dst.flatten(),bins=100)
    # plt.show()

    th = angle<0.996  # was 0.990
    th2 = dst<0.996   # was 0.990

    #Alle waarden die de threshold niet halen worden weer op 0 gezet.
    dummy2 = np.copy(im1)
    dummy2[:,:,0] = dummy2[:,:,0]*th
    dummy2[:,:,1] = dummy2[:,:,1]*th
    dummy2[:,:,2] = dummy2[:,:,2]*th

    dummy1 = np.copy(im1)
    dummy1[:,:,0] = dummy1[:,:,0]*th2
    dummy1[:,:,1] = dummy1[:,:,1]*th2
    dummy1[:,:,2] = dummy1[:,:,2]*th2

    #Hier het resultaat hoe de objecten met de cosinus worden uitgescheden.
#     plt.imshow(dummy2)
#     plt.show()
# 
#     plt.imshow(dummy1)
#     plt.show()

    # Create figure and axes CAN SKIP this
    # fig, ax = plt.subplots()
    # ax.imshow(dummy1)
    # rect = patches.Rectangle((50,100),40,30, linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes Can skip this
    # ax.add_patch(rect)
    # plt.show()

    # IS GEWOON HET SHOWEN VAN DE AFBEELDINGEN
    # background = im1
    # template = dummy1
    # plt.imshow(background)
    # plt.show()
    # plt.imshow(template)
    # # plt.savefig("template.jpg", bbox_inches="tight", pad_inches= 0)
    # plt.show()

    # IS CODE OM BOUNDING BOX VOOR TE BEREIDEN
    test = dummy1 # ASSIGNS PICTURE TO GRAYSCALING
#     plt.imshow(test)
#     plt.show()
    red = test[:,:,0]
    green = test[:,:,1]
    blue = test[:,:,2]

    red = (red/3).astype(int)
    green = (green/3).astype(int)
    blue = (blue/3).astype(int)

    arr2 = red+green+blue

    #print(arr2)

    # BOUDNING BOX CODE!
    y_loc = 0  # index Y = Row
    x_loc = 0  # index X = value in row
    y_cords = []
    x_cords = []

    for row in arr2:
        x_loc = 0
        for value in row:
            if value > 50:
                y_cords.append(y_loc)
                x_cords.append(x_loc)
            #             print(y_loc,x_loc)#, value)
            x_loc += 1
        y_loc += 1

    print()
    # print(y_cords)
    # print(x_cords)

    height = (y_cords[-1] - y_cords[0]) + 1  # +1 want de coordinates zijn index based
    width = x_cords.sort()
    width = (x_cords[-1] - x_cords[0]) + 1  # +1 want de coordinates zijn index based
    #print(x_cords)

    #print("Height:", height, "pixels")
    #print("Width:", width, "pixels")

    x_min = x_cords[0]
    y_min = y_cords[0]

    # print(x_min)
    # print(y_min)


    # Create figure and axes
#     fig, ax = plt.subplots()
#     ax.imshow(test)
#     rect = patches.Rectangle((x_min-1,y_min-1),width+1,height+1, linewidth=1, edgecolor='r', facecolor='none', )

    # Add the patch to the Axes
#     ax.add_patch(rect)
#     plt.axis("off")
#     plt.show()

    # Create figure and axes
    fig, ax = plt.subplots()
    im = ax.imshow(test)

    patch = patches.Rectangle((x_min-1,y_min-1),width+1,height+1,transform=ax.transData)
    im.set_clip_path(patch)

    plt.axis("off")
    
    plt.imsave("OUTGESCHNEDEN_test.jpg", test)
#     print("Al gesaved maar nog niet geshowd")
    plt.show()
    
    img = cv2.imread("OUTGESCHNEDEN_test.jpg")
    cropped_img = img[y_min:(y_min+height), x_min:(x_min+width)]
    
#     cv2.imshow("cropped", cropped_img)
    cv2.imwrite(("cropped_image.jpg"), cropped_img) # code to save template
#     print(y_min, x_min, height, width)
#     print("y_min, x_min, height, width")
    
    # FILE NAMING PART OF THE CODE
    x = 1
    save = False
    while save == False:
        if os.path.exists(f"Templates/template{x}.jpg"):
            x+=1
            #print("Plus one")

        else:
            cv2.imwrite((f"Templates/template{x}.jpg"), cropped_img)
#             plt.savefig(f"Templates/template{x}.jpg")
            save = True
            print(f"template{x} Saved")

    #plt.show()
# makeTemplate()