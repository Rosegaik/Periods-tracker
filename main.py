from tkinter import *
from PIL import Image, ImageTk
import login_user
import signup_user

def login():
    login_user.open_login_window(root)

def signup():
    signup_user.open_signup_window(root)

root = Tk()
root.title('Periods Tracker')
root.geometry('1600x900')
root.resizable(True, True)

# Bg
bg_image = Image.open('signup_bg.jpg')
bg_image = bg_image.resize((1600, 900), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0)

# content
Label(root, text='Welcome to Periods tracker', bg='white', font=('Arial', 20)).place(x=650, y=250)
Button(root, text='Login', width=20, command=login).place(x=700, y=350)
Button(root, text='Signup', width=20, command=signup).place(x=700, y=400)

root.mainloop()
