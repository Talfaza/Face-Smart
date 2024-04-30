import tkinter as tk
import customtkinter as ct
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
cred_workers = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred_workers, name='Workers')


def ui():
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
    header_label.grid(row=0, column=i*2, padx=5, pady=5)

    # Separator line after each header (except last)
    if i < len(headers) - 1:
      separator = ct.CTkFrame(master=app, width=2, height=20, fg_color="gray")  # Option 1: Use fg_color
      # separator = ct.CTkFrame(master=app, width=2, height=20)  # Option 2: Set bg color later
      # separator.configure(bg="gray")  # Option 2: Set background color after creation
      separator.grid(row=0, column=i*2+1, padx=(0, 5), pady=5, sticky="ns")

  # Display workers' information
  if workers_data:
    row = 1
    for worker_id, worker_info in workers_data.items():
      # Create labels for each worker's data
      worker_labels = [worker_id, worker_info.get('name'), worker_info.get('Job'), worker_info.get('Tache'), str(worker_info.get('total_attendence')), worker_info.get('lastAttendenceDate')]
      for i, data in enumerate(worker_labels):
        label = ct.CTkLabel(master=app, text=data)
        label.grid(row=row, column=i*2, padx=5, pady=5)

        # Separator line after each data point (except last)
        if i < len(worker_labels) - 1:
          separator = ct.CTkFrame(master=app, width=2, height=20, fg_color="gray")  # Option 1: Use fg_color
          # separator = ct.CTkFrame(master=app, width=2, height=20)  # Option 2: Set bg color later
          # separator.configure(bg="gray")  # Option 2: Set background color after creation
          separator.grid(row=row, column=i*2+1, padx=(0, 5), pady=5, sticky="ns")
      row += 1
  else:
    label = ct.CTkLabel(master=app, text="No workers found")
    label.grid(row=1, column=0, columnspan=len(headers)*2, padx=5, pady=5)

  app.mainloop()


