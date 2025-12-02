import speech_recognition as sr
import webbrowser
import pygame
import os
from client import client
from musicLib import music
from gtts import gTTS

# ---------------------------------------------------------
# TEXT-TO-SPEECH (AI JARVIS VOICE)
# ---------------------------------------------------------

def speak(text):
    """
    AI Jarvis Voice using OpenAI TTS
    """
    try:
        audio = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        audio.stream_to_file("jarvis_voice.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("jarvis_voice.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove("jarvis_voice.mp3")

    except Exception as e:
        print("TTS Error → using backup voice", e)
        backup = gTTS(text)
        backup.save("backup.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("backup.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove("backup.mp3")


# ---------------------------------------------------------
# OPENAI FALLBACK ANSWER
# ---------------------------------------------------------

def ask_openai(prompt):
    """
    If Jarvis doesn't understand a command,
    this function sends the question to OpenAI.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are Jarvis, an advanced AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I am unable to answer right now."


# ---------------------------------------------------------
# COMMAND PROCESSOR
# ---------------------------------------------------------

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open website" in c:
        webbrowser.open("https://niravprajapati.infinityfreeapp.com")

    elif c.startswith("play"):
        try:
            song = c.split(" ")[1]
            link = music[song]
            webbrowser.open(link)
        except:
            speak("Sorry, I couldn't find that song.")

    elif "open chatgpt" in c:
        webbrowser.open("https://chatgpt.com/")

    else:
        # FALLBACK → Ask OpenAI
        reply = ask_openai(c)
        speak(reply)


# ---------------------------------------------------------
# VOICE ACTIVATION LOOP ("Jarvis")
# ---------------------------------------------------------

if __name__ == "__main__":
    recognizer = sr.Recognizer()

    while True:
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                word = recognizer.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes Sir?")
                    print("Wake word detected. Jarvis Activated.")

                    # Listen for command
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)

                    print("Command:", command)
                    processCommand(command)

        except Exception as e:
            print("Jarvis Error:", e)
