import os
import random
from gtts import gTTS  # pip install gtts
# gtts uses Google Text-to-Speech under the hood (provider identifier in library)

def generate_audio_preview(text, language='en'):
    tts = gTTS(text=text, lang=language)
    filename = f'preview_{random.randint(1000,9999)}.mp3'
    tts.save(filename)
    print(f'Audio preview saved as {filename}')

if __name__ == '__main__':
    generate_audio_preview('Hello, welcome to the service!')