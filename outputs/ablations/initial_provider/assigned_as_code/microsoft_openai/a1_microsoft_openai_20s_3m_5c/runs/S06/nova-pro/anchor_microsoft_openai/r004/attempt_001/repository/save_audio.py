import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def save_audio(audio_bytes, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_bytes)
