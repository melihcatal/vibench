import os

from google.cloud import speech_v1


def transcribe_audio(audio_path: str, language_code: str = "en-US") -> str:
    client = speech_v1.SpeechClient()
    with open(audio_path, "rb") as f:
        content = f.read()
    audio = speech_v1.RecognitionAudio(content=content)
    config = speech_v1.RecognitionConfig(encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3, language_code=language_code)
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results if result.alternatives)
