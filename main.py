import cv2
import os
import pickle
import face_recognition
import numpy as np


# Webcam size function (reusable)
def set_webcam_size(cap, width=640, height=480):
    cap.set(3, width)
    cap.set(4, height)


def run_facial_recognition():
    # Webcam setup
    cap = cv2.VideoCapture(0)
    set_webcam_size(cap)

    # Background image
    imgBack = cv2.imread('ressources/background.png')

    # Models directory
    modelsDir = 'ressources/modules'
    modelsPath = os.listdir(modelsDir)

    # Load model images
    imgModelsList = []
    for name in modelsPath:
        model_path = os.path.join(modelsDir, name)
        model_img = cv2.imread(model_path)
        imgModelsList.append(model_img)

    # Load encoded data from pickle file
    file = open('./encodeFile.p', 'rb')
    encodingListKnownId = pickle.load(file)
    file.close()
    encodingListKnown, workerId = encodingListKnownId

    while True:
        success, img = cap.read()

        # Downscale the image
        smallerImage = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        smallerImage = cv2.cvtColor(smallerImage, cv2.COLOR_BGR2RGB)

        currentFrameFace = face_recognition.face_locations(smallerImage)
        currentFrameEncoding = face_recognition.face_encodings(smallerImage, currentFrameFace)

        # Overlay background and models
        imgBack[162:162 + 480, 55:55 + 640] = img  # Filling webcam in background position
        imgBack[44:44 + 633, 808:808 + 414] = imgModelsList[0]

        # Look through all encodings and compare with pickle encoded files
        for encodedFace, locationFace in zip(currentFrameEncoding, currentFrameFace):
            matching = face_recognition.compare_faces(encodingListKnown, encodedFace)
            distanceFace = face_recognition.face_distance(encodingListKnown, encodedFace)

            # Print results for debugging (optional)
            # print("matching", matching)
            # print("distance", distanceFace)  # the lower the better

            matchingIndex = np.argmin(distanceFace)

            if matching[matchingIndex]:
                # Recognized face
                print(workerId[matchingIndex])
                y1, x2, y2, x1 = locationFace
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # 4 because we downscaled the image by 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

                imgBack = cv2.rectangle(imgBack, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)  # Draw green bounding box

        cv2.imshow("Face Smart", imgBack)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    window_open = False  # Set flag to indicate window is closed
    cv2.destroyAllWindows()

