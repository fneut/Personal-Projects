import cv2
import random 
import numpy as np

scale = 0.5
circles = []
counter = 0
counter2 = 0
point1 = []
point2 = []
myPoints = []
myColor = []
path = '/Users/fneut/Desktop/PP/QueryImages'

def mousePoints(event,x,y,flags,params):
    global counter,point1,point2,counter2,circles,myColor
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter == 0:
            point1 = int(x//scale),int(y//scale)
            counter += 1
            myColor = (random.randint(0,2)*200,random.randint(0,2)*200,random.randint(0,2)*200)
            print("uno")
        elif counter == 1:
            point2 = int(x//scale),int(y//scale)
            name = input('Enter Name ')
            myPoints.append([point1,point2,name])
            counter = 0
            print("dos")
        print(x,",",y)
        circles.append([x,y,myColor])
        counter2 += 1

img = cv2.imread(path + "/" + 'imquery.png')
#img = cv2.resize(img, (0,0), None, scale, scale)
h,w,c = img.shape
img = cv2.resize(img,(w//2,h//2))

while True:
    for x,y,color in circles:
        cv2.circle(img, (x,y), 3, color, cv2.FILLED)
    cv2.imshow("Original Image", img)
    cv2.setMouseCallback("Original Image", mousePoints)
    if cv2.waitKey(1) & 0xff == ord('s'):
        print(myPoints)
        break


