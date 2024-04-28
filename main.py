import cv2
import os
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facesmart1-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "facesmart1.appspot.com"
})
bucket = storage.bucket()

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
    modeType = 0
    id = -1

    # modelType to change the image in the ui
    # counter to check for the match in frames
    # Very first frame counter= 1

    counter = 0
    matchingIndex = None  # Define matchingIndex before the loop
    workersImg = np.zeros((256, 256, 3), dtype=np.uint8)  # Placeholder black image
    start_time = time.time()  # Initialize start time
    update_time = start_time  # Initialize update time

    while True:
        success, img = cap.read()

        # Downscale the image
        smallerImage = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        smallerImage = cv2.cvtColor(smallerImage, cv2.COLOR_BGR2RGB)

        currentFrameFace = face_recognition.face_locations(smallerImage)
        currentFrameEncoding = face_recognition.face_encodings(smallerImage, currentFrameFace)

        # Overlay background and models
        imgBack[162:162 + 480, 55:55 + 640] = img

        # Look through all encodings and compare with pickle encoded files
        for encodedFace, locationFace in zip(currentFrameEncoding, currentFrameFace):
            matching = face_recognition.compare_faces(encodingListKnown, encodedFace)
            distanceFace = face_recognition.face_distance(encodingListKnown, encodedFace)

            matchingIndex = np.argmin(distanceFace)

            if matching[matchingIndex]:
                # Recognized face
                print(workerId[matchingIndex])
                y1, x2, y2, x1 = locationFace
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # 4 because we downscaled the image by 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - x1

                imgBack = cv2.rectangle(imgBack, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                                        (0, 255, 0), 2)  # Draw green bounding box

                modeType = 2  # Set modeType to 2 when face is recognized

        if modeType == 2:
            if time.time() - start_time >= 20:  # Check if 20 seconds have passed
                counter = 0  # Reset counter
                modeType = 1  # Set modeType to 1 after 20 seconds
                start_time = time.time()  # Reset start time
                update_time = time.time()  # Reset update time

        if matchingIndex is not None:
            if counter == 0:
                counter = 1

            if counter != 0:
                if counter == 1:  # first frame
                    id = workerId[matchingIndex]
                    # Getting data from db
                    workersInfo = db.reference(f'Workers/{id}').get()

                    # Getting images from db
                    blob = bucket.get_blob(f'img/{id}.jpg')
                    if blob is not None:
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        workersImg = cv2.imdecode(array, cv2.IMREAD_COLOR)
                        if len(workersImg.shape) == 0:
                            print(f"Empty or corrupted image: img/{id}.jpg")
                            workersImg = np.zeros((256, 256, 3), dtype=np.uint8)  # Create a black image as placeholder
                    else:
                        print(f"Blob img/{id}.jpg does not exist.")
                        workersImg = np.zeros((256, 256, 3), dtype=np.uint8)  # Create a black image as placeholder

                    # Increment attendance or initialize if key doesn't exist
                    if 'total_attendance' in workersInfo:
                        workersInfo['total_attendance'] += 1
                    else:
                        workersInfo['total_attendance'] = 1

                    # Updating data
                    ref = db.reference(f'Workers/{id}')
                    ref.update({'total_attendance': workersInfo['total_attendance']})
                if 10<counter<20:
                    modeType = 2
                    imgBack[44:44 + 633, 808:808 + 414] = imgModelsList[modeType]

                if counter <= 10:
                    imgBack[44:44 + 633, 808:808 + 414] = imgModelsList[1]

                    cv2.putText(imgBack, str(workersInfo['total_attendance']), (820, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(imgBack, str(workersInfo['name']), (930, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (231, 122, 29), 2)  # BGR
                    cv2.putText(imgBack, str(id), (960, 495),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
                    cv2.putText(imgBack, str(workersInfo['Job']), (960, 555),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
                    # Printing image
                    if workersImg is not None and len(workersImg.shape) > 0:
                        imgBack[150:150 + 256, 884:884 + 256] = cv2.resize(workersImg, (256, 256))

                counter += 1  # to keep counting

        cv2.imshow("Face Smart", imgBack)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.getWindowProperty("Face Smart", cv2.WND_PROP_VISIBLE) < 1: # quit window
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_facial_recognition()
