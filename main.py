import speech_recognition as sr
import pyttsx3
import smtplib
import requests
from datetime import datetime

engine=pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command=recognizer.recognize_google(audio)
        print(f"user said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None

def send_email(subject, body, to):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to, message)
            speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

def get_weather(city):
    api_key = "5c55324d84bee64abec4b342a104d726"
    city="London"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
    else:
        speak("City not found.")

def set_reminder(reminder_time, task):
    reminder_datetime = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.now()
    if reminder_datetime > current_datetime:
        time_difference = (reminder_datetime - current_datetime).total_seconds()
        speak(f"Reminder set for {task} at {reminder_time}.")
        import time
        time.sleep(time_difference)
        speak(f"Reminder: {task}")
    else:
        speak("Invalid time for reminder. Please set a future time.")

def handle_command(command):
    if "email" in command:
        speak("What's the subject of the email?")
        subject = recognize_speech()
        speak("What should I say in the email?")
        body = recognize_speech()
        speak("Who should I send it to?")
        to = recognize_speech()
        send_email(subject, body, to)

    elif "weather" in command:
        speak("Which city's weather would you like to know?")
        city = recognize_speech()
        get_weather(city)

    elif "reminder" in command:
        speak("What is the reminder time? (Format: YYYY-MM-DD HH:MM:SS)")
        reminder_time = recognize_speech()
        speak("What is the task?")
        task = recognize_speech()
        set_reminder(reminder_time, task)

    else:
        speak("Sorry, I can only handle emails, weather updates, and reminders right now.")

if __name__ == "__main__":
    while True:
        speak("How can I assist you?")
        command = recognize_speech()

        if command:
            handle_command(command)

        else:
            speak("Please Try Again")
