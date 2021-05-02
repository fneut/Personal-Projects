import cv2
import os
import numpy as np 
import pytesseract as tess
import csv


path = '/Users/fneut/Desktop/PP/QueryImages'
myPicList = os.listdir(path)
print(myPicList)


for z,k in enumerate(myPicList):
    if(z == 1):
        nombre_foto = k

myData = []
myData2 = []

def RegionInteres(contador):
    global roi,j
    if contador == 0:
        j = 0
    else:
        j += 50
    roi = [[(0,j), (89, 50+j), 'fecha'],
    [(126, j), (285, 50+j), 'descripcion'], 
    [(402, j), (538, 50+j), 'canal'], 
    [(623, j), (731, 50+j), 'cargos'], 
    [(780, j), (878, 50+j), 'abono'], 
    [(916, j), (1015, 50+j), 'saldo']]

RegionInteres(0)

imgQ = cv2.imread(path + "/" + str(nombre_foto))
h,w,c = imgQ.shape
imgQ = cv2.resize(imgQ,(w//2,h//2))
cv2.imshow("output", imgQ)

imgShow = imgQ.copy()
imgMask = np.zeros_like(imgShow)

print(f' ############### Extrayendo data de la imagen {nombre_foto} ###############')

for veces in range(9):
    #print(roi)
    for sub,r in enumerate(roi):
        #cv2.rectangle(imgMask,r[0],r[1],(0,255,0), cv2.FILLED)
        cv2.rectangle(imgMask,(r[0][0],r[0][1]),(r[1][0],r[1][1]) ,(0,255,0), cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
        imgCrop = imgQ[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        myData.append(tess.image_to_string(imgCrop))    
    myData.append('\n\n\x0c')
    myData2.append(myData)
    myData = []
    RegionInteres(1)


print(myData2)  
with open('/Users/fneut/Desktop/PP/SalidaData.csv','a+' ) as f:
    for num,contenido in enumerate(myData2):
        if(num != 0):
            for num2,contenido2 in enumerate(contenido):
                if(num2 == 6):
                    f.write(str(contenido2)[:-2])
                else:
                    f.write(str(contenido2)[:-2]+',')
   

imgShow = cv2.resize(imgShow,(w//3,h//3))
cv2.imshow("output2", imgShow)    
cv2.waitKey(0)

