import os
import wave
from audioop import rms

from speech_client import TextToSpeechClient


def synthesize_plain_text(text: str, voice_name: str = None) -> bytes:
    """Synthesize plain text to an audio byte stream using the configured provider.

    Args:
        text (str): The plain text to synthesize.
        voice_name (str, optional): Optional voice name to use.

    Returns:
        bytes: Raw PCM audio data.
    """
    client = TextToSpeechClient()
    response = client.synthesize_speech(
        input_text=text,
        voice_name=voice_name,
    )
    # Assuming response provides raw audio bytes (e.g., WAV or PCM)
    return response.audio_bytes
