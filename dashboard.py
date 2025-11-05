from tkinter import *
from PIL import Image, ImageTk
import session
from entry import open_add_period_window
from calendar_view import view_calendar
from chart_view import open_chart_window
from chatbot import open_chatbot

def open_dashboard(master):
    master.withdraw()
    win = Toplevel()
    win.title("Period Tracker Dashboard")
    win.geometry("1600x800")
    win.configure(bg="white")

    # Background Image (optional)
    bg_image = Image.open("signup_bg.jpg")  # Optional background image
    bg_image = bg_image.resize((1600, 800))
    bg = ImageTk.PhotoImage(bg_image)
    bg_label = Label(win, image=bg)
    bg_label.place(x=0, y=0)

    # Greeting
    greeting = Label(win, text=f"Welcome, {session.name}!", font=("Arial", 22, "bold"), fg="#d6336c", bg="white")
    greeting.place(x=700, y=40)

    # Add Period Button
    add_btn = Button(win, text="➕ Add Period", font=("Arial", 14), bg="#ffccd5", fg="black", width=20, command=lambda: open_add_period_window(win))
    add_btn.place(x=700, y=130)

    # View Periods (Calendar)
    view_btn = Button(win, text="📅 View Calendar", font=("Arial", 14), bg="#ffe5ec", fg="black", width=20, command=lambda: view_calendar(win))
    view_btn.place(x=700, y=190)

    # Chart
    chart_btn = Button(win, text="📊 View Chart", font=("Arial", 14), bg="#e2eafc", fg="black", width=20, command=lambda: open_chart_window(win))
    chart_btn.place(x=700, y=250)

    # ChatBot
    chat_btn = Button(win, text="💬 ChatBot (Symptoms Help)", font=("Arial", 14), bg="#d0f4de", fg="black", width=25, command=lambda: open_chatbot(win))
    chat_btn.place(x=675, y=310)

    # Logout Button
    def logout():
        session.current_user_id = None
        session.name = None
        win.destroy()
        master.deiconify()

    logout_btn = Button(win, text="🚪 Logout", font=("Arial", 12), bg="#ccc", fg="black", command=logout)
    logout_btn.place(x=1400, y=20)

    win.mainloop()
