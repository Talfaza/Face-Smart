import cv2
import face_recognition
import pickle
import os
from PIL import Image

# Function to resize images to 250x250
def resize_image(image):
    return image.resize((250, 250))

#importing images
path = 'img'
modelsPath = os.listdir(path)


# Resize images first
for id in modelsPath:
    model_path = os.path.join(path, id)
    img = Image.open(model_path)

    # Check if image size is 250x250, if not, resize it
    if img.size != (250, 250):
        img = resize_image(img)
        img.save(model_path)

imgModelsList = []
workerId = []
for id in modelsPath:
    model_path = os.path.join(path, id)
    model_img = cv2.imread(model_path)
    imgModelsList.append(model_img)
    #print(os.path.splitext(id)[0])
    workerId.append(os.path.splitext(id)[0])
print(len(imgModelsList))

#print(workerId)


def encodingGen(imgModelsList):
    encodingList = []
    for img in imgModelsList:
        #transform to rgb ( cv2  bgr face recog uses rgb )
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encodingList.append(encoding)
    return encodingList
("Strating to encode")
encodingListKnown = encodingGen(imgModelsList)
encodingListKnownId = [encodingListKnown, workerId]

file = open("encodeFile.p", 'wb')
pickle.dump(encodingListKnownId, file)
file.close()
print("Pickle File Dumpeb")


print("Finish")
print(encodingListKnown)