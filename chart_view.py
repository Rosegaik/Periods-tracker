from tkinter import messagebox
from connection import get_connection
import session
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def open_chart_window(master):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        user_id = session.current_user_id
        cursor.execute("""
            SELECT period_date, duration, cycle_length 
            FROM periods 
            WHERE user_id = %s 
            ORDER BY period_date ASC
        """, (user_id,))
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No period entries to show in chart.")
            return

        # Extract data
        dates = [row[0] for row in data]
        durations = [row[1] for row in data]
        cycles = [row[2] if row[2] else 28 for row in data]

        # Format x-axis labels
        labels = [d.strftime('%d-%b-%Y') if isinstance(d, datetime) else str(d) for d in dates]
        x = np.arange(len(labels))

        bar_width = 0.4

        # Plot
        plt.figure(figsize=(12, 6))
        bars1 = plt.bar(x - bar_width/2, durations, width=bar_width, color='crimson', label='Duration (days)')
        bars2 = plt.bar(x + bar_width/2, cycles, width=bar_width, color='steelblue', label='Cycle Length (days)')

        # Annotate values and period date range
        for i, (dx, start_date, dur, cyc) in enumerate(zip(x, dates, durations, cycles)):
            end_date = start_date + timedelta(days=dur - 1)
            range_text = f"{start_date.strftime('%d-%b')} → {end_date.strftime('%d-%b')}"
            plt.text(dx - bar_width/2, dur + 0.5, str(dur), ha='center', va='bottom', fontsize=8, color='crimson')
            plt.text(dx + bar_width/2, cyc + 0.5, str(cyc), ha='center', va='bottom', fontsize=8, color='steelblue')
            plt.text(dx, max(dur, cyc) + 1.5, range_text, ha='center', va='bottom', fontsize=8, color='black', rotation=30)

        # Labels and style
        plt.title(f"{session.name}'s Period Tracker", fontsize=14)
        plt.xlabel("Period Date", fontsize=12)
        plt.ylabel("Days", fontsize=12)
        plt.xticks(ticks=x, labels=labels, rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Chart Error:", e)
        messagebox.showerror("Error", f"Could not load chart.\n{e}")

    finally:
        if conn:
            conn.close()
