
import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import model
import camera

class Prog:

    def __init__(self, window=tk.Tk()):

        self.window = window
        self.window.title('Image recognition')

        self.counter = [1, 1, 1]

        self.model = model.Model()

        self.auto_predict = False

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15
        self.update()
        
        self.window.mainloop()

    def init_gui(self):

        
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack(anchor=tk.CENTER) 

        self.object_one = simpledialog.askstring("object One", "Enter the name of the first object:", parent=self.window)
        self.object_two = simpledialog.askstring("object Two", "Enter the name of the second object:", parent=self.window)
        
        self.btn_class_one = tk.Button(self.window, text=self.object_one, width=60, command=lambda: self.save_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER)

        self.btn_class_two = tk.Button(self.window, text=self.object_two, width=60, command=lambda: self.save_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER)

        self.btn_train = tk.Button(self.window, text="Train Model", width=60, command=lambda: self.model.train(self.counter))
        self.btn_train.pack(anchor=tk.CENTER)
        
        self.btn_class_zero = tk.Button(self.window, text="Background", width=60, command=lambda: self.save_class(3))
        self.btn_class_zero.pack(anchor=tk.CENTER)

        self.btn_predict = tk.Button(self.window, text="Predcit", width=60, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER)

        self.btn_auto = tk.Button(self.window, text="Auto Prediction", width=60, command=self.auto_prediction)
        self.btn_auto.pack(anchor=tk.CENTER)

        self.btn_reset = tk.Button(self.window, text="Reset", width=60, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER)

        self.class_label = tk.Label(self.window, text="None")
        self.class_label.config(font=("Arial", 30))
        self.class_label.pack(anchor=tk.CENTER)


    def auto_prediction(self):
        self.auto_predict = not self.auto_predict

    def save_class(self, class_num):
        ret, frame = self.camera.current_frame()
        if not os.path.exists("object1"):
            os.mkdir("object1")
        if not os.path.exists("object2"):
            os.mkdir("object2")
        if not os.path.exists("object3"):
            os.mkdir("object3")

    
        cv.imwrite(f'object{class_num}/frame{self.counter[class_num-1]}.jpg', cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        img = PIL.Image.open(f'object{class_num}/frame{self.counter[class_num - 1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'object{class_num}/frame{self.counter[class_num - 1]}.jpg')

        self.counter[class_num - 1] += 1

    def reset(self):
        for folder in ['object1', 'object2' ,'object3']:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        self.counter = [1, 1, 1]
        self.model = model.Model()
        self.class_label.config(text="")

    def update(self):
        if self.auto_predict:
            print(self.predict())

        ret, frame = self.camera.current_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.current_frame()
        prediction = self.model.predict(frame)

        if prediction == 1:
            self.class_label.config(text=self.object_one)
            return self.object_one
        if prediction == 2:
            self.class_label.config(text=self.object_two)
            return self.object_two
        if prediction == 3:
            self.class_label.config(text="Nothing")
            return "Background"