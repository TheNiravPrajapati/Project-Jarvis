import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLib
import pygame
import os
from gtts import gTTS

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()

    pygame.mixer.music.load('temp.mp3')

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open website" in c.lower():
        webbrowser.open("https://niravprajapati.infinityfreeapp.com")
    elif c.lower().startswith("play"):
        song = c.lower.split(" ")[1]
        link = musicLib.music[song]
        webbrowser.open(link)
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com/")
    else: 
        speak("Currently I am Under Construction")

if __name__ == "__main__":

    # Listen Wake Up Word
    while True: 
        r = sr.Recognizer() 
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                if(word.lower() == "jarvis"):
                    speak("Ya Buddy")
                    with sr.Microphone() as source:
                        print("Jarvis Activated")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)

            processCommand(command)

        except Exception as e:
            print(f"Jarvis Error: {e}")