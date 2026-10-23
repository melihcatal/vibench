from google.cloud import texttospeech


def save_audio(audio_bytes, file_path):
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_bytes)