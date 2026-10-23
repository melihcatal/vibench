# tts_qa_transcript.py
# [LATER-STEP]
# Transcribe synthesized QA samples using Google Cloud Speech-to-Text to verify spoken output.

import os
from google.cloud import speech_v1p1beta1 as speech

# Utility from same-scenario helpers
from speech_client import TextToSpeechClient  # placeholder import for consistency

STT_MODEL = "default"  # can be swapped for enhanced models like 'phone_call'

def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """Transcribe raw audio bytes to plain text.
    Args:
        audio_bytes: binary audio (e.g., MP3) produced by TTS.
        language_code: BCP-47 language identifier (default en-US).
    Returns:
        The best transcription result.
    """
    client = speech.SpeechClient()
    # Convert MP3 to linear16 PCM as required by STT (strip headers)
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=language_code,
        model=STT_MODEL,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcription = response.results[0].alternatives[0].transcript
    return transcription


def verify_qa(qa_prompt: str, synthesized_audio: bytes) -> bool:
    """Check that the TTS output matches the expected QA prompt.
    Performs transcription and simple equality check.
    Returns True if transcription equals prompt (case-insensitive)."
    transcribed = transcribe_audio(synthesized_audio, language_code="en-US")
    return transcribed.strip().lower() == qa_prompt.strip().lower()
