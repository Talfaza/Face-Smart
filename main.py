import pickle
import cv2
import os
import face_recognition
import numpy as np
import cvzone

#webcam size
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
#importing images
imgBack = cv2.imread('ressources/background.png')

modelsDir = 'ressources/modules'
modelsPath = os.listdir(modelsDir)

imgModelsList = []
for name in modelsPath:
    model_path = os.path.join(modelsDir, name)
    model_img = cv2.imread(model_path)
    imgModelsList.append(model_img)
#import pickle encoded file

file = open('./encodeFile.p', 'rb')
encodingListKnownId = pickle.load(file)
file.close()
encodingListKnown, workerId = encodingListKnownId

#print(workerId)


#print(len(imgModelsList))
while True:
    success, img = cap.read()
    #downscale the image

    smallerImage = cv2.resize(img, (0,0), None, 0.25, 0.25)
    smallerImage = cv2.cvtColor(smallerImage , cv2.COLOR_BGR2RGB)

    currentFrameFace = face_recognition.face_locations(smallerImage)
    currentFrameEncoding = face_recognition.face_encodings(smallerImage,currentFrameFace)

    imgBack[162:162+480,55:55+640] = img # filling webcam in backgound position imgBack[startWidth:endWidth, heigh,heigh]
    imgBack[44:44+633,808:808+414] = imgModelsList[0]

    #look through all the encodings and compare it with pickle encoded files

    for encodedFace, locationFace in zip(currentFrameEncoding, currentFrameFace):

        matching = face_recognition.compare_faces(encodingListKnown,encodedFace)
        distanceFace = face_recognition.face_distance(encodingListKnown,encodedFace)

        print("matching", matching)
        print("distance", distanceFace) #the lower the better

        """
        get a matching index then compare it the value in the matching if the value
        is True then the face is detected
        """
        matchingIndex = np.argmin(distanceFace)
        print(matchingIndex)


        if matching[matchingIndex]:
            #print("Known Face ! ! ! ! ! ! ! ")
            print(workerId[matchingIndex])
            y1, x2, y2, x1 = locationFace
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #4 because we downscale the image by 4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1

            imgBack = cvzone.cornerRect(imgBack, bbox,rt=0)


    cv2.imshow("Face Smart",imgBack)
    cv2.waitKey(1)