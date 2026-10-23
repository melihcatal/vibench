import pyttsx3


def generate_spoken_brief(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()