from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio
import os


def transcribe_audio_from_bytes(
    audio_content: bytes, language_code: str = "en-US"
) -> str:
    client = speech.SpeechClient()
    audio = RecognitionAudio(content=audio_content)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    transcripts = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcripts)


def transcribe_audio_from_gcs(gcs_uri: str, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = RecognitionAudio(uri=gcs_uri)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    transcripts = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcripts)
