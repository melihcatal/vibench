import os
from google.cloud import speech

def submit_transcription(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print(f'Operation name: {operation.name}')
    return operation.name