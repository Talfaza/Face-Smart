import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from firebase_admin import db
import adminUI

def delete_worker():
    def delete_from_db():
        worker_id = entry_id.get()
        if not worker_id:
            messagebox.showwarning("Error", "Please enter the worker ID.")
            return

        ref = db.reference('Workers')
        ref.child(worker_id).delete()
        messagebox.showinfo("Success", f"Worker with ID {worker_id} has been deleted.")
        app.destroy()
        adminUI.ui()

    app = ctk.CTk()
    app.title("Supprimer")
    app.geometry("400x150")

    # Create labels and entry widgets for "ID"
    label_id = ctk.CTkLabel(master=app, text="ID:")
    label_id.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_id = ctk.CTkEntry(master=app)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    # Create a button to delete worker
    button_delete = ctk.CTkButton(master=app, text="Delete Worker", command=delete_from_db)
    button_delete.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    app.mainloop()

