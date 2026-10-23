import os
from google.cloud import speech_v1 as speech

def submit_transcription(audio_file_path):
    client = speech.SpeechClient()
    config = {"encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
               "sample_rate_hertz": 16000,
               "language_code": "en-US"}
    audio = {"uri": audio_file_path}
    response = client.long_running_recognize(config=config, audio=audio)
    return response.name