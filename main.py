import os
import pickle
import face_recognition
import numpy as np
import cv2
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

bucket = storage.bucket()
def run_facial_recognition():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    imgBackground = cv2.imread('ressources/background.png')

    # Importing the mode images into a list
    folderModePath = 'ressources/modules'
    modePathList = os.listdir(folderModePath)
    imgModeList = []
    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
    # print(len(imgModeList))

    # Load the encoding file
    print("Loading Encode File ...")
    file = open('encodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, workersId = encodeListKnownWithIds
    # print(workersId)
    print("Encode File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print("matches", matches)
                # print("faceDis", faceDis)

                matchIndex = np.argmin(faceDis)
                # print("Match Index", matchIndex)

                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(workersId[matchIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = workersId[matchIndex]
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

            if counter != 0:

                if counter == 1:
                    # Get the Data
                    wrokersInfo = db.reference(f'Workers/{id}').get()
                    print(wrokersInfo)
                    # Get the Image from the storage
                    blob = bucket.get_blob(f'img/{id}.jpg')
                    if blob is None:
                        print(f"Error: Image for student with ID {id} not found in storage!")
                        continue
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    # Update data of attendance
                    datetimeObject = datetime.strptime(wrokersInfo['lastAttendenceDate'],
                                                       "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Workers/{id}')
                        wrokersInfo['total_attendence'] += 1
                        ref.child('total_attendence').set(wrokersInfo['total_attendence'])
                        ref.child('total_attendence').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:

                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(wrokersInfo['lastAttendenceDate']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(wrokersInfo['name']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(wrokersInfo['Job']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(wrokersInfo['Tache']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(wrokersInfo['Tache']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(wrokersInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(wrokersInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        wrokersInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0
        # cv2.imshow("Webcam", img)
        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)