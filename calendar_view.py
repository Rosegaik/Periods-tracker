from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from connection import get_connection
import session
from datetime import datetime, timedelta
from entry import open_add_period_window  # ✅ make sure this accepts prefill_date

def view_calendar(master):
    win = Toplevel(master)
    win.title("Period Calendar View")
    win.geometry("600x500")
    win.configure(bg="white")

    Label(win, text=f"{session.name}'s Period Calendar", font=("Arial", 16, "bold"), bg="white").place(x=150, y=20)

    cal = Calendar(win, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    cal.place(x=150, y=80)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        user_id = session.current_user_id
        cursor.execute("SELECT id, period_date, duration, notes, cycle_length FROM periods WHERE user_id = %s ORDER BY period_date ASC", (user_id,))
        data = cursor.fetchall()

        period_map = {}

        for row in data:
            id, date, duration, notes, cycle = row
            date_str = date.strftime("%Y-%m-%d")
            period_map[date_str] = row

            # 🔴 Mark all days of duration in red
            for i in range(duration):
                cal.calevent_create(date + timedelta(days=i), 'Period', 'period')

        cal.tag_config('period', background='red', foreground='white')

        # ✅ Predict multiple future periods
        if data:
            last = data[-1]
            last_date = last[1]
            last_duration = last[2]
            cycle_length = last[4] or 28  # Default if missing

            for i in range(1, 7):  # Predict next 6 months
                next_date = last_date + timedelta(days=i * cycle_length)
                for j in range(last_duration):
                    cal.calevent_create(next_date + timedelta(days=j), 'Predicted', 'predicted')

            cal.tag_config('predicted', background='green', foreground='white')

    except Exception as e:
        print("DB Error:", e)
        Label(win, text="Error loading calendar.", fg="red", bg="white").place(x=200, y=450)

    def on_date_select(event):
        selected_date = cal.get_date()
        selected_str = datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")

        if selected_str in period_map:
            entry = period_map[selected_str]
            open_edit_popup(entry)
        else:
            result = messagebox.askyesno("Add New Entry", f"No entry exists for {selected_str}.\nDo you want to add one?")
            if result:
                win.destroy()
                open_add_period_window(master, prefill_date=selected_str)

    def open_edit_popup(entry):
        id, period_date, duration, notes, cycle = entry
        popup = Toplevel(win)
        popup.title("Edit Period Entry")
        popup.geometry("400x300")
        popup.configure(bg="white")

        Label(popup, text="Edit Period", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        Label(popup, text="New Period Date", bg="white").pack()
        new_date = DateEntry(popup)
        new_date.set_date(period_date)
        new_date.pack(pady=5)

        Label(popup, text="Duration (days)", bg="white").pack()
        duration_entry = Entry(popup)
        duration_entry.insert(0, str(duration))
        duration_entry.pack(pady=5)

        Label(popup, text="Notes", bg="white").pack()
        notes_entry = Text(popup, height=3, width=30)
        notes_entry.insert("1.0", notes)
        notes_entry.pack(pady=5)

        def save_changes():
            try:
                updated_date = new_date.get_date()
                updated_duration = int(duration_entry.get())
                updated_notes = notes_entry.get("1.0", END).strip()

                cursor = get_connection().cursor()
                cursor.execute("""
                    SELECT period_date FROM periods
                    WHERE user_id = %s AND period_date < %s
                    ORDER BY period_date DESC LIMIT 1
                """, (session.user_id, updated_date))
                prev = cursor.fetchone()
                new_cycle = (updated_date - prev[0]).days if prev else None

                cursor.execute("""
                    UPDATE periods
                    SET period_date = %s, duration = %s, notes = %s, cycle_length = %s
                    WHERE id = %s AND user_id = %s
                """, (updated_date, updated_duration, updated_notes, new_cycle, id, session.user_id))
                cursor.connection.commit()
                cursor.close()
                popup.destroy()
                win.destroy()
                view_calendar(master)
                messagebox.showinfo("Updated", "Period entry updated successfully!")
            except Exception as e:
                print("Update error:", e)
                messagebox.showerror("Error", "Failed to update entry.")

        Button(popup, text="Save Changes", command=save_changes).pack(pady=10)

    cal.bind("<<CalendarSelected>>", on_date_select)

    win.mainloop()
