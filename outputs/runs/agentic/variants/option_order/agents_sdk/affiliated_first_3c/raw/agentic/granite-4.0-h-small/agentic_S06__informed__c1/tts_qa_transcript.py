import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_bytes):
    """Transcribe synthesized speech audio to verify the QA output using Google Cloud Speech-to-Text.
    Args:
        audio_bytes (bytes): Raw audio data (e.g., LINEAR16).
    Returns:
        str: Recognized transcript.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US',
        enable_automatic_punctuation=True
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ' '.join(result.alternatives[0].transcript for result in response.results)
    return transcript
