import pyrebase
import tkinter 
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")
app.title("Face_id")


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

class FaceApp(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)

        
        self.side_frame=customtkinter.CTkFrame(self)
        self.side_frame.pack(side="left",fill="y")
        self.label=customtkinter.CTkLabel(self.side_frame,text="Se Connecter avec:",font=("stylus", 16, "bold"))
        self.label.pack(pady=50,padx=30)

        self.button_code = customtkinter.CTkButton(master=self.side_frame, text="Face Recognation",border_color="blue",fg_color="#262626",corner_radius=12,border_width=2,width=140,height=32,font=("stylus",13))
        self.button_code.pack(pady=12, padx=10)

        self.button_Face = customtkinter.CTkButton(master=self.side_frame, text="Mot de passe",border_color="blue",fg_color="#262626",corner_radius=12,border_width=2,width=140,height=32,font=("stylus",13))
        self.button_Face.pack(pady=12, padx=10)



class Login_face(FaceApp):
    def __init__(self):
        FaceApp.__init__(self)



        
        def login():
            print("login")
            self.email = self.username_entry.get()
            self.password = self.password_entry.get()

            try:
                self.user = auth.sign_in_with_email_and_password(self.email, self.password)
                self.result.configure(text="You logged in successfully!")
            except Exception as e:
                self.error_message = str(e)
                if "INVALID_EMAIL" in self.error_message:
                    self.result.configure(text="Invalid email format. Please enter a valid email.")
                elif "INVALID_PASSWORD" in self.error_message:
                    self.result.configure(text="Incorrect password. Please try again.")
                elif "USER_NOT_FOUND" in self.error_message:
                   self.result.configure(text="User not found. Please register.")
                else:
                   self.result.configure(text="Error")


        self.frame = customtkinter.CTkFrame(self)  # Indented consistently
        self.frame.pack(pady=10, padx=60, fill="both", expand=True)

        self.frame1 = customtkinter.CTkFrame(master=self.frame, fg_color="#262626", corner_radius=10)
        self.frame1.pack(pady=150, padx=160, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame1, text="Login System", font=("stylus", 30, "bold"))
        self.label.pack(pady=20, padx=10)
        self.username_entry = customtkinter.CTkEntry(master=self.frame1, placeholder_text="Username", width=140, height=30)
        self.username_entry.pack(pady=12, padx=10)
        self.password_entry = customtkinter.CTkEntry(master=self.frame1, placeholder_text="Password", show="*", width=140, height=30)
        self.password_entry.pack(pady=12, padx=10)
        self.button = customtkinter.CTkButton(master=self.frame1, text="Login", command=login)  # Ensure 'login' is defined
        self.button.pack(pady=12, padx=10)

        self.result = customtkinter.CTkLabel(master=self.frame1, text="", corner_radius=8)
        self.result.pack(pady=12, padx=10)


    def login():
        print("login")
        self.email = username_entry.get()
        self.password = password_entry.get()

        try:
            self.user = auth.sign_in_with_email_and_password(email, password)
            self.result.configure(text="You logged in successfully!")
        except Exception as e:
            self.error_message = str(e)
            if "INVALID_EMAIL" in self.error_message:
                self.result.configure(text="Invalid email format. Please enter a valid email.")
            elif "INVALID_PASSWORD" in self.error_message:
                self.result.configure(text="Incorrect password. Please try again.")
            elif "USER_NOT_FOUND" in self.error_message:
                self.result.configure(text="User not found. Please register.")
            else:
                self.result.configure(text="Error")

        




        

app=FaceApp()
app.mainloop()
