import random
import os
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog
import firebase_admin
from firebase_admin import credentials

def Ajouter():
    def resize_image(image_path, size=(250, 250)):
        try:
            image = Image.open(image_path)
            image_resized = image.resize(size)
            return image_resized
        except Exception as e:
            print("Error resizing image:", e)
            return None

    def upload_image():
        # Generate a random 4-digit number for the image name
        random_number = random.randint(1000, 9999)
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "img"),
                                               filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            # Get the file name and extension
            file_name = os.path.basename(file_path)
            file_extension = file_name.split(".")[-1]
            # Construct the new file name with the random number and extension
            new_file_name = f"{random_number}.{file_extension}"
            # Move the image to the 'img' folder with the new name
            new_file_path = os.path.join(os.getcwd(), "img", new_file_name)
            os.rename(file_path, new_file_path)

            # Resize the image
            resized_image = resize_image(new_file_path)
            if resized_image:
                resized_image.save(new_file_path)  # Overwrite the original image with the resized one

            # Debugging
            # print("Selected file:", file_path)
            # print("New file name:", new_file_name)

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
        # Get the values from the entry widgets
        nom = entry_nom.get()
        job = entry_job.get()
        tache = entry_tache.get()

        # Add your logic here to use the entered values (e.g., add to the database)
        print("Nom:", nom)
        print("Job:", job)
        print("Tache:", tache)

        # Close the window after processing
        app.destroy()

    # Create a button to submit the values
    button_submit = ctk.CTkButton(master=app, text="Submit", command=on_button_click)
    button_submit.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Start the Tkinter event loop
    app.mainloop()
