import pyrebase
import tkinter 
import customtkinter

customtkinter.set_appearance_mode("black")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")

side_frame=customtkinter.CTkFrame(app)
side_frame.pack(side="left",fill="y")
label=customtkinter.CTkLabel(side_frame,text="dashboard")
label.pack(pady=50,padx=40)

firebaseConfig = {
    'apiKey': "AIzaSyC1L5Kzv4NPV7cMLvH6rZmGHE043-x5fBA",
    'authDomain': "faceid-88932.firebaseapp.com",
    'projectId': "faceid-88932",
    'storageBucket': "faceid-88932.appspot.com",
    'messagingSenderId': "99319735026",
    'appId': "1:99319735026:web:cb88ce3b4295ada2ed266b",
    'measurementId': "G-3510VPGC02",
    "databaseURL": " "
}

# Setting up the application
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    print("login")
    email = username_entry.get()
    password = password_entry.get()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        result.configure(text="You logged in successfully!")
    except Exception as e:
        error_message = str(e)
        if "INVALID_EMAIL" in error_message:
            result.configure(text="Invalid email format. Please enter a valid email.")
        elif "INVALID_PASSWORD" in error_message:
            result.configure(text="Incorrect password. Please try again.")
        elif "USER_NOT_FOUND" in error_message:
            result.configure(text="User not found. Please register.")
        else:
            result.configure(text="Error")

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)
label = customtkinter.CTkLabel(master=frame, text="Login System",font=("Arial", 16, "bold"))
label.pack(pady=12, padx=10)
username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username",width=120,height=25)
username_entry.pack(pady=12, padx=10)
password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*",width=120,height=25)
password_entry.pack(pady=12, padx=10)
button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)
result = customtkinter.CTkLabel(master=frame,
                                text="",
                                corner_radius=8)
result.pack(pady=12, padx=10)



app.mainloop()
