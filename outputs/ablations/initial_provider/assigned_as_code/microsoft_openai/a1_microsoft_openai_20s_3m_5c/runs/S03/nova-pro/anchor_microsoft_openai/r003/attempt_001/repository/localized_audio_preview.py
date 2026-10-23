import requests
import pyttsx3


def localized_audio_preview(translation):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(translation['text'])
    engine.runAndWait()