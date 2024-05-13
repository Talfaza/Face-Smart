import random
import os
from PIL import Image
import customtkinter as ctk
import tkinter
from tkinter import filedialog
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import cv2
import face_recognition
import pickle
from datetime import datetime
import adminUI
new_file_path = ""
idWorker = ""




def Ajouter():
    # Function to resize images to 250x250
    def resize_image(image):
        return image.resize((216, 216))

    # Function to encode faces in images
    def encode_faces(image_path):
        model_img = cv2.imread(image_path)
        # Resize image if necessary
        img = Image.open(image_path)
        if img.size != (216, 216):
            img = resize_image(img)
            img.save(image_path)  # Overwrite the original image with the resized one

        # Encode face if face is detected
        img = cv2.cvtColor(model_img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            encoding = face_encodings[0]
            return encoding
        else:
            print("No face detected in the uploaded image.")
            return None

    bucket = storage.bucket()

    def upload_image():
        print("Upload image button clicked")  # Debugging statement
        # Generate a random 4-digit number for the image name
        random_number = random.randint(1000, 9999)
        global idWorker

        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "img"),
                                               filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            # Get the file name and extension
            file_name = os.path.basename(file_path)
            file_extension = file_name.split(".")[-1]
            # Construct the new file name with the random number and extension
            new_file_name = f"{random_number}.{file_extension}"
            # Move the image to the 'img' folder with the new name
            global new_file_path
            new_file_path = os.path.join(os.getcwd(), "img", new_file_name)
            os.rename(file_path, new_file_path)

            # Encode the uploaded image
            encoding = encode_faces(new_file_path)

            # Dump the encoded face to a pickle file
            with open("encodeFile.p", "ab") as pickle_file:
                pickle.dump({new_file_name: encoding}, pickle_file)
            # Debugging
            print("Encoded face saved to pickle file.")

            # Open the image again for resizing
            img = Image.open(new_file_path)

            # Resize the image
            resized_image = resize_image(img)
            if resized_image:
                resized_image.save(new_file_path)  # Overwrite the original image with the resized one

            # Assign the image name to idWorker
            global idWorker
            idWorker = os.path.splitext(new_file_name)[0]

            # Upload the image to Firebase Storage with content type "application/octet-stream"
            firebase_folder = 'img'
            blob = bucket.blob(firebase_folder + '/' + new_file_name)
            blob.upload_from_filename(new_file_path, content_type="application/octet-stream")

            # Debugging
            print("Image uploaded to Firebase Storage:", blob.public_url)

    # Create the main window
    app = ctk.CTk()
    app.title("Ajouter")
    app.geometry("400x400")  # Set the size of the window

    # Create labels and entry widgets for "nom", "job", and "tache"
    label_nom = ctk.CTkLabel(master=app, text="Nom:")
    label_nom.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nom = ctk.CTkEntry(master=app)
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    label_job = ctk.CTkLabel(master=app, text="Job:")
    label_job.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_job = ctk.CTkEntry(master=app)
    entry_job.grid(row=1, column=1, padx=5, pady=5)

    label_tache = ctk.CTkLabel(master=app, text="Tache:")
    label_tache.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_tache = ctk.CTkEntry(master=app)
    entry_tache.grid(row=2, column=1, padx=5, pady=5)

    # Create a button to upload image
    button_upload = ctk.CTkButton(master=app, text="Upload Image", command=upload_image)
    button_upload.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Function to handle the button click
    def on_button_click():
        print("Submit button clicked")  # Debugging statement
        # Get the values from the entry widgets
        nom = entry_nom.get()
        job = entry_job.get()
        tache = entry_tache.get()

        # Add your logic here to use the entered values
        print("Nom:", nom)
        print("Job:", job)
        print("Tache:", tache)

        # Get current date as a string
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Construct data object
        data = {
            idWorker: {
                'name': nom,
                'Job': job,
                'Tache': tache,
                'total_attendence': 1,
                'lastAttendenceDate': current_date

            }
        }

        # Upload data to Realtime Database
        ref = db.reference('Workers')
        for key, val in data.items():
            ref.child(key).set(val)

        # Close the window after processing
        app.destroy()
        adminUI.ui()

    # Create a button to submit the values
    button_submit = ctk.CTkButton(master=app, text="Submit", command=on_button_click)
    button_submit.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Start the Tkinter event loop
    app.mainloop()

