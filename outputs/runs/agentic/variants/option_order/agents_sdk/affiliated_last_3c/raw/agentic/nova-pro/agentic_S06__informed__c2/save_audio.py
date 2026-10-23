import os

def save_audio(audio_content, file_name):
    with open(file_name, 'wb') as f:
        f.write(audio_content)