import session
from tkinter import *
from tkinter import messagebox
#from PIL import Image,ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql
from connection import get_connection


'''def open_entry_window(master):
    user_id=session.current_user_id
    #print(user_id)
    win=Toplevel(master)
    win.title('Periods Date entry')
    win.geometry('1600x900')
    #bg
    bg_image=Image.open('signup_bg.jpg')
    bg_image=bg_image.resize((1600,900),Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label=Label(win,image=bg_photo)
    bg_label.image=bg_photo
    bg_label.place(x=0,y=0)

    form_bg='white'
    Label'''

# Replace with actual user ID after login
#user_id = session.current_user_id

def open_add_period_window(master,prefill_date=None):
    add_window = Toplevel(master)
    add_window.title("Add Period Entry")
    add_window.geometry("400x400")
    add_window.config(bg="#f8f0f2")

    # Period Date
    Label(add_window, text="Period Date:", bg="#f8f0f2").place(x=30, y=30)
    date_entry = DateEntry(add_window, width=20, date_pattern='yyyy-mm-dd', background='darkblue',
                           foreground='white', borderwidth=2)
    date_entry.place(x=180, y=30)

    # Cycle Length
    Label(add_window, text="Cycle Length (days):", bg="#f8f0f2").place(x=30, y=80)
    entry_cycle = Entry(add_window, width=22)
    entry_cycle.place(x=180, y=80)

    # Duration
    Label(add_window, text="Duration (days):", bg="#f8f0f2").place(x=30, y=130)
    entry_duration = Entry(add_window, width=22)
    entry_duration.place(x=180, y=130)

    # Notes
    Label(add_window, text="Notes:", bg="#f8f0f2").place(x=30, y=180)
    entry_notes = Entry(add_window, width=22)
    entry_notes.place(x=180, y=180)

    # Save Data Function
    def save_data():
        period_date = date_entry.get_date()
        cycle_length = entry_cycle.get()
        duration = entry_duration.get()
        notes = entry_notes.get()

        if not cycle_length or not duration:
            messagebox.showerror("Input Error", "Please fill all required fields.")
            return

        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO periods (user_id, period_date, cycle_length, duration, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (session.current_user_id, period_date, cycle_length, duration, notes))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Period entry saved successfully!")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Save Button
    Button(add_window, text="Save Entry", command=save_data, bg="#4CAF50", fg="white", width=20).place(x=120, y=250)


    


    
    
