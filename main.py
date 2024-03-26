import cv2
import os
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBack = cv2.imread('ressources/background.png')

modelsDir = 'ressources/modules'
modelsPath = os.listdir(modelsDir)

imgModelsList = []
for name in modelsPath:
    model_path = os.path.join(modelsDir, name)
    model_img = cv2.imread(model_path)
    imgModelsList.append(model_img)

print(len(imgModelsList))
while True:
    success, img = cap.read()
    imgBack[162:162+480,55:55+640] = img
    cv2.imshow("Face Smart",imgBack)
    cv2.waitKey(1)