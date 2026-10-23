# diarized_transcript.py
import os
import requests

# Provider: Google Cloud Speech-to-Text (provider identifiable via client library and credentials)
from google.cloud import speech_v1p1beta1 as speech


def diarized_transcript(audio_path):
    """Request speaker diarization for a recorded meeting.

    Returns the diarized transcript JSON.
    """
    client = speech.SpeechClient()
    # Load audio file
    with open(audio_path, "rb") as f:
        content = f.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
        diarization_request_id="meeting_diarization",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results
