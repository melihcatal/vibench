from google.cloud import speech_v1p1beta1 as speech
import os
from typing import Dict, Any

def transcribe_audio_from_uri(gcs_uri: str, language_code: str = "en-US") -> Dict[str, Any]:
    """Transcribes synthesized QA samples from a GCS URI to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 as common output from TTS
        sample_rate_hertz=16000, # This might need adjustment based on TTS output
        language_code=language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for transcription operation to complete...")
    response = operation.result(timeout=90)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return {"transcript": transcript.strip()}

def transcribe_audio_from_bytes(audio_bytes: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000) -> Dict[str, Any]:
    """Transcribes synthesized QA samples from audio bytes to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 from TTS
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return {"transcript": transcript.strip()}

