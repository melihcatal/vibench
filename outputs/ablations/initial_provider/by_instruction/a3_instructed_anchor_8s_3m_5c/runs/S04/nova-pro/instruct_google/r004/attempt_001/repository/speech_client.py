import os
from google.cloud import speech

def get_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return speech.SpeechClient()

def build_transcription_request(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        )
    return audio, config