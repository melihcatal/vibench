# [LATER-STEP] tts_qa_transcript.py

import os
from typing import Optional
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_bytes: bytes, sample_rate_hertz: int = 24000) -> str:
    """Transcribe synthesized audio to text using Google Cloud Speech-to-Text for QA verification.

    Args:
        audio_bytes: Raw audio bytes produced by TTS synthesis.
        sample_rate_hertz: Sample rate of the audio (default 24kHz for many TTS outputs).

    Returns:
        Recognized transcription as a string.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcription = response.results[0].alternatives[0].transcript
    return transcription
