import pyttsx3

engine = pyttsx3.init()


def generate_spoken_brief(text):
    engine.say(text)
    engine.runAndWait()
