from os.path import commonpath
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import webbrowser
import requests
import json
import re
import os
import smtplib
import spotipy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  recommender.api import Recommender, _ClientCredentialsFlow
from spotipy.oauth2 import SpotifyClientCredentials


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def name():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as main:
            engine.say("What's your name?")
            engine.runAndWait()
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(main, duration=0)
            print("Please, Say your name...")
            audio = r.listen(main, timeout=5.0)
            saying_name = r.recognize_google(audio, language='en-in').lower()
            print(saying_name)

            if "" in saying_name:
                filtering = saying_name.replace("my name is", "")
                intro = f"Hey {filtering}, Alexa is here\n "
                hour = int(datetime.datetime.now().hour)
                if hour >= 0 and hour < 12:
                    speak(intro + "Good Morning")
                elif hour >= 12 and hour < 18:
                    speak(intro + "Good Afternoon")
                else:
                    speak(intro + "Good Evening")

    except:
        pass

name()


listener = sr.Recognizer()
microphone = sr.Microphone()


class Alexa:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.microphone = sr.Microphone()

    def take_command(self, listener, microphone):
        try:
            with microphone as source:
                print("\nListening..")
                listener.adjust_for_ambient_noise(source, duration=1)
                listener.dynamic_energy_threshold = 3000
                voice = listener.listen(source)
                command = listener.recognize_google(voice).lower()

                if "alexa" in command:
                    command.replace('alexa', '')
                    return alexa.run_alexa(command)

                elif "alexa" not in command:
                    print(command)
                    engine.say("You should call me alexa first")
                    engine.runAndWait()

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Slow internet Connection")


    def talk(self, text):
        engine.say(text)
        engine.runAndWait()
         

    def run_alexa(self, command):
        if "play" in command:
            print(command)
            song = command.replace('alexa play', '')
            print("Playing " + song)
            alexa.talk("playing" + song)
            pywhatkit.playonyt(song)

        elif "time" in command:
            print(command)
            time = datetime.datetime.now().strftime('%H:%M')
            com = "The time is"
            print(com + time)
            alexa.talk(com + time)

        elif "search" in command:
            print(command)
            try:
                rep = "According to wikipedia, "
                info = command.replace("alexa search", "")
                search = wikipedia.summary(info, 1)
                print(rep + search)
                alexa.talk(rep + search)
            except wikipedia.exceptions.PageError:
                raise Exception("Sorry, Wikipedia couldn't fetch your information")

        elif "recommend" in command:
            print(command)
            songs = ["rock", "pop", "metalcore", "song", "chill", "dj", "hip-hop", "r&b"]
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= "ed147dfb315f4ab3a0dbbd0607667f68", client_secret="a1897520673842f99d8261a9d69e604e"))
            results = sp.search(q=random.choice(songs), limit=1)
            for idx, track in enumerate(results['tracks']['items']):
                saying = (track["name"], "by",  track["artists"][0]["name"])
                print(saying)
                alexa.talk(saying)


        elif "joke" in command:
            print(command)
            joke = pyjokes.get_joke()
            print(joke)
            alexa.talk(joke)

        elif "web search" in command:
            print(command)
            search_for = command.split("alexa web search", 1)[1]
            url = "https://duckduckgo.com/"
            urll = url + "/" + search_for
            webbrowser.open(urll)
            alexa.talk("Done")

        elif "music" in command:
            music_dir = ""
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            
        elif "chrome" in command:
            path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            alexa.talk("opening Google Chrome...")
            os.startfile(path)

        elif "where is" in command:
            cut = command.split()
            location_url = f"https://www.google.com/maps/plcace/{cut[2]}"
            response = alexa.talk("Holf on pal\n I'm searching it")
            maps_args = webbrowser.open(location_url)
            os.system(maps_args)

        elif "activity" in command:
            print(command)
            response = requests.get("https://www.boredapi.com/api/activity")
            data = json.loads(response.content)
            activity = data["activity"]
            typof = data["type"]
            ac = activity
            print(ac)
            alexa.talk(ac)

        elif "weather" in command:
            response = requests.get(
                "http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json")
            dt = json.loads(response.content)
            print(dt)
            alexa.talk(dt)

        elif "age" in command:
            c = "age"
            response = requests.get(f"https://api.agify.io?name={c}")
            data = json.loads(response.content)
            age = data["age"]
            print(age)
            alexa.talk(age)

        elif "quote of the day" in command:
            print(command)
            response = requests.get("https://zenquotes.io/api/random")
            data = json.loads(response.content)
            qu = data[0]["q"]
            by = data[0]["a"]
            print(f"{qu}, quote by {by}")
            alexa.talk(f"{qu}, quote by {by}")
        
        def mail(to, msg):
            server = smtplib.SMTP("smpt.gmail.com", 587)
            server.echo()
            server.starttls()
            server.login("your@email.com", "password")
            server.sendmail("your@email.com", to, msg)
            server.close()

            if "mail" in command:
                try:
                    alexa.talk("Whats the mail?")
                    msg = command
                    to = "denmarkz922@gmail.com"
                    mail(to, msg)
                except Exception as ex:
                    print(ex)
                    alexa.talk("Sorry, unable to proceed ")


    def how(self, command):
        print(command)
        ask = ["how are you", "how you doing",
               "what's up", "how are you doing"]
        if random.choice(ask) in command:
            greetings = ["I'm Good", "chilling", "never better", "always fine"]
            gr = random.choice(greetings)
            print(gr)
            alexa.talk(gr)

if __name__ == "__main__":
    alexa = Alexa()

    while True:
        command = alexa.take_command(listener, microphone)
