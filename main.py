import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
from groq import Groq

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "Your API KEY"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_news(api_key, category=None):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    if category:
        url += f"&category={category}"

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])
        if articles:
            for article in articles:
                print(article['title'])
                speak(article['title'])
        else:
            speak(f"No news articles found for the category {category}.")
    else:
        speak("Failed to retrieve news")


def extract_category(command):
    keywords = ["news about", "news on", "news related to"]
    for keyword in keywords:
        if keyword in command.lower():
            category = command.lower().split(keyword)[-1].strip()
            return category
    return None


def aiProcess(command):
    client = Groq(
        api_key="Your API KEY",)

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis , skilled in general tasks like Alexa and Google Cloud. Give short responses"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content


def process_command(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
         
    elif "news" in c.lower():
        category = extract_category(c)
        get_news(newsapi, category)
    else:
        # Let OpenAi handle the request
        output = aiProcess(c)
        print(output)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "hello" or word.lower() == "Jarvis" or word.lower() == "jaarvis" or word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    process_command(command)
        except Exception as e:
            print("Error; {0}".format(e))
