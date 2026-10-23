import pyttsx3


def generate_spoken_brief(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

