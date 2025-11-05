from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from connection import get_connection
import session
import dashboard

def open_login_window(master):
    win = Toplevel(master)
    win.title("Login Page")
    win.geometry("1600x900")

    # Background
    bg_image = Image.open("login_bg.jpg")
    bg_image = bg_image.resize((1600, 900), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(win, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0)

    form_bg = "white"

    Label(win, text="Login Form", font=("Arial", 24, "bold"), bg=form_bg).place(x=680, y=200)

    Label(win, text="Email:", font=("Arial", 14), bg=form_bg).place(x=600, y=280)
    email_entry = Entry(win, font=("Arial", 14), width=30)
    email_entry.place(x=720, y=280)

    Label(win, text="Password:", font=("Arial", 14), bg=form_bg).place(x=600, y=330)
    password_entry = Entry(win, font=("Arial", 14), show="*", width=30)
    password_entry.place(x=720, y=330)

    def login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                con = get_connection()
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
                result = cur.fetchone()
                if result is not None:
                    session.current_user_id = result[0]
                    session.name=result[1]
                    messagebox.showinfo("Success", "Login Successful!")
                    win.destroy()
                    from dashboard import open_dashboard
                    dashboard.open_dashboard(master)
                else:
                    messagebox.showerror("Error", "Invalid email or password")
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"Database Error: {str(e)}")
              

    Button(win, text="Login", font=("Arial", 14), bg="blue", fg="white", width=20, command=login)\
        .place(x=720, y=400)
    
