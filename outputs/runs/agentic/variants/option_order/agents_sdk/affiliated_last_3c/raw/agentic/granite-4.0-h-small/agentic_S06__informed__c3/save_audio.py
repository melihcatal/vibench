import os

def save_audio(audio_data, output_path):
    with open(output_path, 'wb') as f:
        f.write(audio_data)
