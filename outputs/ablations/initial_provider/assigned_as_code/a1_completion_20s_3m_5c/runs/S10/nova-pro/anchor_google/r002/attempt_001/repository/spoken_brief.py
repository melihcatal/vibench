import os
from gtts import gTTS


def generate_spoken_brief(payload):
    tts = gTTS(text=payload["text"], lang='en')
    tts.save('spoken_brief.mp3')
    return {"file": 'spoken_brief.mp3'}