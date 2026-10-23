import os
from elevenlabs import Client

def generate_speech(text):
    client = Client(os.getenv('ELEVENLABS_API_KEY'))
    audio = client.text_to_speech(text)
    return audio