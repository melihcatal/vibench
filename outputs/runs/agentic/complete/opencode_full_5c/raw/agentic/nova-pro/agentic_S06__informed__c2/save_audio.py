import os


def save_audio(audio_data, file_path):
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)
