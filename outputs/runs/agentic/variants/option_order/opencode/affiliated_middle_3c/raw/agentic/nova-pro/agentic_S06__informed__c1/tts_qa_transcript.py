import os
from google.cloud import speech_v1


def transcribe_audio(audio_content):
    client = speech_v1.SpeechClient()
    audio = speech_v1.RecognitionAudio(content=audio_content)
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3, language_code="en-US"
    )
    response = client.recognize(config, audio)
    return " ".join([result.alternatives[0].transcript for result in response.results])
