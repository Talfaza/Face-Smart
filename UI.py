import customtkinter as ct

# Flag to track login section visibility (initially hidden)
is_login_visible = False

# Function to toggle login section visibility
def toggle_login():
    global is_login_visible
    # ... your existing toggle_login function implementation (from previous code)

# Function to start facial recognition when the button is clicked
def start_face_recognition():
    import main  # Assuming face_recognition.py is in the same directory
    main.run_facial_recognition()

# Create the main window
app = ct.CTk()
app.state('zoomed')
app.geometry("800x600")
app.title("Face Smart")

# **Create a frame to group the login section (optional for better organization):**
login_frame = ct.CTkFrame(master=app)
login_frame.pack(pady=20)  # Add padding for spacing

# Create styled title label (optional)
title_label = ct.CTkLabel(master=login_frame, text="Face Smart", font=("Arial", 20))
title_label.pack(pady=20)  # Add padding for spacing

# Create styled subtitle label (optional)
subtitle_label = ct.CTkLabel(master=login_frame, text="Login", font=("Arial", 16))
subtitle_label.pack(pady=10)  # Add top and bottom padding

# Create a frame for ID section (placed within login_frame)
id_frame = ct.CTkFrame(master=login_frame)
id_frame.pack(pady=10)  # Add padding for spacing

# Create ID label within the frame
id_label = ct.CTkLabel(master=id_frame, text="ID:")
id_label.pack(side="left", padx=5)  # Pack on the left with padding

# Create ID entry within the frame
id_entry = ct.CTkEntry(master=id_frame, placeholder_text="Enter ID")
id_entry.pack(side="left", expand=True, padx=10)  # Add left and right padding

# Create a frame for password section (similar approach, placed within login_frame)
password_frame = ct.CTkFrame(master=login_frame)
password_frame.pack(pady=10)  # Add padding for spacing

password_label = ct.CTkLabel(master=password_frame, text="PASSWORD:")
password_label.pack(side="left", padx=5)

password_entry = ct.CTkEntry(master=password_frame, show="*", placeholder_text="Enter Password")
password_entry.pack(side="left", expand=True, padx=10)  # Add left and right padding

# Login button
login_button = ct.CTkButton(master=login_frame, text="Login!")
login_button.pack(pady=10)  # Add bottom padding

# **Create and add buttons to the top-left corner:**
loginButtonMenu = ct.CTkButton(master=app, text="Login", command=toggle_login)
loginButtonMenu.place(relx=0.0, rely=0.01, anchor="nw")

faceButtonMenu = ct.CTkButton(master=app, text="Face Smart", command=start_face_recognition)
faceButtonMenu.place(relx=0.0, rely=0.1, anchor="nw")

# Separator line
window_width = app.winfo_width()
custom_color = "#1D7AE7"
separator = ct.CTkFrame(master=app, width=2, height=2000, fg_color=custom_color)
separator.place(relx=0.2, rely=0.0)

# Create "test" label (initially hidden)
test_label = ct.CTkLabel(master=login_frame, text="test", font=("Arial", 20))
test_label.pack_forget()

# Run the main loop
app.mainloop()
