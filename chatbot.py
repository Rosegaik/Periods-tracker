from tkinter import *
from tkcalendar import DateEntry
import pyttsx3
import speech_recognition as sr
from datetime import datetime, timedelta
import session
from connection import get_connection
from tkinter import messagebox

def open_chatbot(master):
    win = Toplevel(master)
    win.title("Period Tracker Chatbot")
    win.geometry("1600x800")
    win.configure(bg="#121212")  # Dark background

    # Chat area
    chat_area = Text(win, width=180, height=52, wrap=WORD,
                     bg="#1e1e1e", fg="white", font=("Arial", 16))
    chat_area.place(x=30, y=30)

    # Entry field
    entry = Entry(win, width=120, font=("Arial", 25),
                  bg="#333333", fg="white", insertbackground="white")
    entry.place(x=30, y=740)

    # Text-to-Speech setup
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 170)
    tts_engine.setProperty('volume', 1)
    voices = tts_engine.getProperty('voices')
    if len(voices) > 1:
        tts_engine.setProperty('voice', voices[1].id)

    def get_next_period_info():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            user_id = session.current_user_id
            cursor.execute(
                "SELECT period_date, cycle_length FROM periods WHERE user_id = %s ORDER BY period_date DESC LIMIT 1",
                (user_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                last_date = row[0]
                cycle_length = row[1]
                next_period = last_date + timedelta(days=cycle_length)
                return f"Your next period is expected around: {next_period.strftime('%d %B %Y')}"
            else:
                return "I don't have enough data to predict your next period."
        except Exception:
            return "Error fetching data."

    def get_reply():
        user_input = entry.get().lower()
        reply = "Sorry, I didn’t understand that."

        if "hello" in user_input or "hi" in user_input:
            reply = "Hi! I'm your period buddy. How can I help you today?"
        elif "cramp" in user_input:
            reply = "Try placing a hot water bag on your lower abdomen. Gentle stretches may help too."
        elif "headache" in user_input:
            reply = "Make sure you're hydrated and try resting in a quiet place. A warm drink might help!"
        elif "bloating" in user_input:
            reply = "Avoid salty food and drink more water. Peppermint tea can be soothing!"
        elif "acne" in user_input:
            reply = "Try to keep your face clean and avoid oily foods. Hormonal changes can trigger breakouts."
        elif "mood" in user_input or "angry" in user_input:
            reply = "It’s okay to feel emotional during your cycle. Take deep breaths, listen to music, or rest."
        elif "tired" in user_input or "fatigue" in user_input:
            reply = "Your body needs more rest during your period. Try to sleep well and eat iron-rich food."
        elif "food craving" in user_input:
            reply = "Craving sweets? Try dark chocolate or fruits. Just enjoy it in moderation!"
        elif "tip" in user_input:
            reply = "Tip: Keep a small period emergency kit with pads, meds, and snacks when going out."
        elif "nausea" in user_input:
            reply = "Try ginger tea or small frequent meals. Nausea is common during early days of period."
        elif "period delay" in user_input:
            reply = "Stress, diet, or health changes can delay periods. If delay continues, consult a doctor."
        elif "next period" in user_input:
            reply = get_next_period_info()
        elif "thank" in user_input:
            reply = "You're always welcome! 😊"
        elif "bye" in user_input:
            reply = "Bye! Stay strong and take care ❤"

        chat_area.insert(END, f"You: {user_input}\nBot: {reply}\n\n")
        entry.delete(0, END)

        tts_engine.say(reply)
        tts_engine.runAndWait()

    def listen_to_voice():
        recognizer = sr.Recognizer()
        message = ""  

        with sr.Microphone() as source:
            chat_area.insert(END, "Bot: Listening...\n")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                entry.delete(0, END)
                entry.insert(0, user_input)
                get_reply()
                return  
            except sr.WaitTimeoutError:
                message = "I didn't hear anything."
            except sr.UnknownValueError:
                message = "Sorry, I couldn't understand."
            except sr.RequestError as e:
                message = f"Speech service error: {e}"

            chat_area.insert(END, f"Bot: {message}\n\n")
            tts_engine.say(message)
            tts_engine.runAndWait()

    # Buttons (larger size for full screen)
    Button(win, text="Send", font=("Arial", 14, "bold"), bg="#444", fg="white", width=12,
           height=2, command=get_reply).place(x=1200, y=735)

    Button(win, text="🎤 Speak", font=("Arial", 14, "bold"), bg="#444", fg="white", width=12,
           height=2, command=listen_to_voice).place(x=1350, y=735)
