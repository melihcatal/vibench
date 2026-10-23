from gtts import gTTS
import os


def generate_audio_preview(text, language="en"):
    tts = gTTS(text=text, lang=language)
    tts.save("preview.mp3")
    os.system("afplay preview.mp3")
