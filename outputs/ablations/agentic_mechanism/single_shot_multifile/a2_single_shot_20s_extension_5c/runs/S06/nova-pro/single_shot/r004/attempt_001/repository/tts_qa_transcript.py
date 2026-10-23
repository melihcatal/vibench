import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def transcribe_audio(audio_content):
    config = {"encoding": speech.RecognitionConfig.AudioEncoding.MP3, "sample_rate_hertz": 16000, "language_code": "en-US"}
    audio = {"content": audio_content}
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript