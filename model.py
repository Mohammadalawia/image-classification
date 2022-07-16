
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import cv2 as cv
import PIL

class Model:

    def __init__(self):
        self.model = KNeighborsClassifier(n_neighbors=5)

    def train(self, counter):
        img_list = np.array([])
        class_list = np.array([])

        for i in range(1, counter[0]):
            img = cv.imread(f'object1/frame{i}.jpg')[:,:,0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 1)

        for i in range(1, counter[1]):
            img = cv.imread(f'object2/frame{i}.jpg')[:,:,0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 2)

        for i in range(1,counter[2]):
            img = cv.imread(f'object3/frame{i}.jpg')[:,:,0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 3)


        img_list = img_list.reshape(counter[0] - 1 + counter[1] - 1 + counter[2] - 1, 16950)
        self.model.fit(img_list, class_list)
        print("Trained successfully!")

    def predict(self, frame):
        frame = frame[1]
        cv.imwrite("prediction.jpg", cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        img = PIL.Image.open("prediction.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save("prediction.jpg")

        img = cv.imread('prediction.jpg')[:,:,0]
        img = img.reshape(16950)
        prediction = self.model.predict([img])

        return prediction[0]