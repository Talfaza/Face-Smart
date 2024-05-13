import customtkinter as ct
from firebase_admin import db
import ajouter
import modifier
import supprimer

def open_ajouter_window():
    # Function to open the "Ajouter" window
    app.destroy()
    ajouter.Ajouter()
def open_modifier_window():
    app.destroy()
    modifier.update_database()

def open_supprimier_windows():
    app.destroy()
    supprimer.delete_worker()


def ui():
    global app
    app = ct.CTk()

    app.title("Workers Viewer")
    app.geometry("800x600")

    # Retrieve data from the 'Workers' database
    reference_workers = db.reference('Workers')
    workers_data = reference_workers.get()

    # Define column headers
    headers = ["ID", "Name", "Job", "Tache", "Total Attendance", "Last Attendance"]

    # Create header labels and separators
    for i, header in enumerate(headers):
        header_label = ct.CTkLabel(master=app, text=header)
        header_label.grid(row=0, column=i * 2, padx=5, pady=5)

        # Separator line after each header (except last)
        if i < len(headers) - 1:
            separator = ct.CTkFrame(master=app, width=2, height=20, fg_color="gray")
            separator.grid(row=0, column=i * 2 + 1, padx=(0, 5), pady=5, sticky="ns")

    # Display workers' information
    if workers_data:
        row = 1
        for worker_id, worker_info in workers_data.items():
            # Create labels for each worker's data
            worker_labels = [worker_id, worker_info.get('name'), worker_info.get('Job'),
                             worker_info.get('Tache'), str(worker_info.get('total_attendence')),
                             worker_info.get('lastAttendenceDate')]
            for i, data in enumerate(worker_labels):
                label = ct.CTkLabel(master=app, text=data)
                label.grid(row=row, column=i * 2, padx=5, pady=5)

                # Separator line after each data point (except last)
                if i < len(worker_labels) - 1:
                    separator = ct.CTkFrame(master=app, width=2, height=20, fg_color="gray")
                    separator.grid(row=row, column=i * 2 + 1, padx=(0, 5), pady=5, sticky="ns")
            row += 1
    else:
        label = ct.CTkLabel(master=app, text="No workers found")
        label.grid(row=1, column=0, columnspan=len(headers) * 2, padx=5, pady=5)

    # Create three buttons on the right side with padding
    button1 = ct.CTkButton(master=app, text="Ajouter", command=open_ajouter_window)
    button1.grid(row=0, column=len(headers) * 2 + 1, padx=(100, 0), pady=(5, 5), sticky="e")

    button2 = ct.CTkButton(master=app, text="Supprimer",command=open_supprimier_windows)
    button2.grid(row=1, column=len(headers) * 2 + 1, padx=(100, 0), pady=(5, 5), sticky="e")

    button3 = ct.CTkButton(master=app, text="Modifier",command=open_modifier_window)
    button3.grid(row=2, column=len(headers) * 2 + 1, padx=(100, 0), pady=(5, 5), sticky="e")
    app.mainloop()

