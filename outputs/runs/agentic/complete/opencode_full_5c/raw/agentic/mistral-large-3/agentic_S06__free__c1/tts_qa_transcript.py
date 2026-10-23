from google.cloud import speech_v1p1beta1 as speech
import os
from typing import Union


def tts_qa_transcript(audio_content: bytes, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)

    transcript = "".join(
        result.alternatives[0].transcript for result in response.results
    )
    return transcript
