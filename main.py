import cv2
import numpy as np
import os
import time
import HandTracking_Mod as tr

path = "Images"
Pictures = os.listdir("Images")
print(Pictures)
imlist = []
brushThickness = 15
eraserThisckness = 70
for impath in Pictures:
    image = cv2.imread(f'{path}/{impath}')
    imlist.append(image)

header = imlist[0]
color_paint = (0,0,0)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = tr.handDetector(detectionCon=0.85)
imgCanvas = np.zeros((720,1280,3),np.uint8)
xp = 0
yp = 0
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)

    # find Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = True)

    if len(lmList)!=0:
        print(lmList)

        x1,y1 = lmList[8][1:] # tip of index finger coordinates
        x2,y2 = lmList[12][1:]


        # check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        # if Selectio mode : Two fingers are up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print("Select Mode is On")
            if y1<125:
                if 133 <x1< 307:
                    header = imlist[0]
                    color_paint = (94,23,235)
                elif 438 <x1 <610 :
                    header = imlist[1]
                    color_paint = (255,22,22)
                elif 702 <x1< 869 :
                    header = imlist[2]
                    color_paint = (126, 217, 87)
                elif 1015 <x1<1161 :
                    header = imlist[3]
                    color_paint = (0,0,0)


            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), color_paint, cv2.FILLED)

        # if Drawing Mode : Index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),55,color_paint,cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0 :
                xp,yp = x1,y1

            if color_paint == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), color_paint, eraserThisckness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color_paint, eraserThisckness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),color_paint,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),color_paint,brushThickness)


            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    img[0:125,0:1280] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)

