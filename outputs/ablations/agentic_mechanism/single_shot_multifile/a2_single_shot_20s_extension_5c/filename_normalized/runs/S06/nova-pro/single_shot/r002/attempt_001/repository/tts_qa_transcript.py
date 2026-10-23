import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_content):
    client = speech.SpeechClient()
    audio = speech.types.RecognitionAudio(content=audio_content)
    config = speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.MP3,
                                             language_code='en-US')
    response = client.recognize(config=config, audio=audio)
    return ' '.join([result.alternatives[0].transcript for result in response.results])