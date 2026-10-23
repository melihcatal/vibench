import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                                      language_code='en-US')
    response = client.recognize(config=config, audio=audio)
    return ' '.join([result.alternatives[0].transcript for result in response.results])
