
import json
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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def name():
    r = sr.Recognizer()
    with sr.Microphone() as main:
        engine.say("What's your name?")
        engine.runAndWait()
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(main, duration=0)
        print("Please, Say your name...")
        audio = r.listen(main)
        saying_name = r.recognize_google(audio).lower()
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
            raise Exception("it's a temporary error, Try Again")
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

        if "time" in command:
            time = datetime.datetime.now().strftime('%H:%M')
            com = "Right now it's "
            print(com + time)
            alexa.talk(com + time)

        if "search" in command:
            print(command)
            rep = "According to wikipedia, "
            info = command.replace("alexa search", "")
            search = wikipedia.summary(info, 1)
            print(rep + search)
            alexa.talk(rep + search)

        if "joke" in command:
            print(command)
            joke = pyjokes.get_joke()
            print(joke)
            alexa.talk(joke)

        if "open google" in command:
            reg_ex = re.search("open google (.*)", command)
            search_for = command.split("google", 1)[1]
            url = "https://www.google.com"
            if reg_ex:
                google = reg_ex.group(1)
                url = url + "/" + google
            webbrowser.open(url)
            alexa.talk("Done")
            # driver = webdriver.Firefox(executable_path='/pqth/to/geckodriver')
            # driver.get("https://www.google.com")
            # search = driver.find_element_by_id('q')
            # search.send_keys(str(search_for))
            # search.send_keys(Keys.RETURN)

        if "where is" in command:
            cut = command.split()
            location_url = f"https://www.google.com/maps/plcace/{cut[2]}"
            response = alexa.talk("Holf on pal\n I'm searching it")
            maps_args = webbrowser.open(location_url)
            os.system(maps_args)

        if "activity" in command:
            response = requests.get("https://www.boredapi.com/api/activity")
            data = json.loads(response.content)
            activity = data["activity"]
            typof = data["type"]
            ac = activity
            print(ac)
            alexa.talk(ac)

        if "weather" in command:
            response = requests.get(
                "http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json")
            dt = json.loads(response.content)
            print(dt)
            alexa.talk(dt)

        if "age" in command:
            c = "age"
            response = requests.get(f"https://api.agify.io?name={c}")
            data = json.loads(response.content)
            age = data["age"]
            print(age)
            alexa.talk(age)

        if "quote of the day" in command:
            response = requests.get("https://zenquotes.io/api/random")
            data = json.loads(response.content)
            qu = data[0]["q"]
            by = data[0]["a"]
            print(f"{qu}, quote by {by}")
            alexa.talk(f"{qu}, quote by {by}")

    def how(self, command):
        ask = ["how are you", "how you doing",
               "what's up", "how are you doing"]
        if random.choice(ask) in command:
            greetings = ["I'm Good", "chilling", "never better", "always fine"]
            gr = random.choice(greetings)
            print(gr)
            alexa.talk(gr)


alexa = Alexa()

while True:
    command = alexa.take_command(listener, microphone)
