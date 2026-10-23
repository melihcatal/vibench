import os
from google.cloud import speech_v1 as speech


def transcribe_qa_sample(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, "rb") as f:
        audio_content = f.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code="en-US"
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join([result.alternatives[0].transcript for result in response.results])
