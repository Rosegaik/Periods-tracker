from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from connection import get_connection

def open_signup_window(master):
    win = Toplevel(master)
    win.title("Signup Page")
    win.geometry("1600x900")

    # Background
    bg_image = Image.open("login_bg.jpg")
    bg_image = bg_image.resize((1600, 900), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(win, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0)

    Label(win, text="Signup Form", font=("Arial", 24, "bold"), bg="white").place(x=670, y=100)

    Label(win, text="Name:", font=("Arial", 14), bg="white").place(x=600, y=180)
    name_entry = Entry(win, font=("Arial", 14), width=30)
    name_entry.place(x=720, y=180)

    Label(win, text="Phone:", font=("Arial", 14), bg="white").place(x=600, y=230)
    phone_entry = Entry(win, font=("Arial", 14), width=30)
    phone_entry.place(x=720, y=230)

    Label(win, text="Email:", font=("Arial", 14), bg="white").place(x=600, y=280)
    email_entry = Entry(win, font=("Arial", 14), width=30)
    email_entry.place(x=720, y=280)

    Label(win, text="Password:", font=("Arial", 14), bg="white").place(x=600, y=330)
    password_entry = Entry(win, font=("Arial", 14), show="*", width=30)
    password_entry.place(x=720, y=330)

    def signup():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if name == "" or phone == "" or email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                con = get_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO users (name, phone, email, password) VALUES (%s, %s, %s, %s)",
                            (name, phone, email, password))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Registration successful!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}")

    Button(win, text="Signup", font=("Arial", 14), bg="green", fg="white", width=20, command=signup)\
        .place(x=720, y=400)
