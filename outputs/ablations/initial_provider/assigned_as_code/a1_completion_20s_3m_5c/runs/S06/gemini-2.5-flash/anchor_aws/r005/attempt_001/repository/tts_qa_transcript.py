from google.cloud import speech_v1p1beta1 as speech
import io
import os

def transcribe_audio_sample(audio_bytes: bytes, sample_rate_hertz: int, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript
