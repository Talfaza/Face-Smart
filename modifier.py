import tkinter as tk
from firebase_admin import db, initialize_app, credentials
import customtkinter as ctk
import adminUI


def update_database():

    def update_db():
        # Get values from input fields
        student_id = id_entry.get()
        name = name_entry.get()
        job = job_entry.get()
        task = task_entry.get()

        # Check if the ID exists in the database
        ref = db.reference('Workers')
        student = ref.child(student_id).get()
        if student:
            # Update the values in the database
            ref.child(student_id).update({
                'name': name,
                'Job': job,
                'Tache': task
            })
            tk.messagebox.showinfo("Success", "Database updated successfully!")
        else:
            tk.messagebox.showerror("Error", "ID not found in the database!")
        app.destroy()
        adminUI.ui()

    # Create the main window
    app = ctk.CTk()
    app.title("Modifier")
    app.geometry("400x400")  # Set the size of the window

    # Create labels and entry widgets for "ID", "Name", "Job", and "Task"
    label_id = ctk.CTkLabel(master=app, text="ID:")
    label_id.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    id_entry = ctk.CTkEntry(master=app)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    label_nom = ctk.CTkLabel(master=app, text="Name:")
    label_nom.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = ctk.CTkEntry(master=app)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    label_job = ctk.CTkLabel(master=app, text="Job:")
    label_job.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    job_entry = ctk.CTkEntry(master=app)
    job_entry.grid(row=2, column=1, padx=5, pady=5)

    label_tache = ctk.CTkLabel(master=app, text="Task:")
    label_tache.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    task_entry = ctk.CTkEntry(master=app)
    task_entry.grid(row=3, column=1, padx=5, pady=5)

    # Create a button to submit the values
    button_submit = ctk.CTkButton(master=app, text="Submit", command=update_db)
    button_submit.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Start the Tkinter event loop
    app.mainloop()

