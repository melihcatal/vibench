import os
from model_client import get_platform_client

def generate_audio(output_text):
    client = get_platform_client()
    audio_data = client.text_to_speech(output_text)
    return audio_data