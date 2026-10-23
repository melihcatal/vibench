import os
from google.cloud import texttospeech_v1

def get_speech_client() -> texttospeech_v1.TextToSpeechClient:
    """
    Provides a configured Google Cloud Text-to-Speech client.
    """
    return texttospeech_v1.TextToSpeechClient()

def get_default_voice_config() -> dict:
    """
    Returns default voice configuration.
    """
    return {
        "language_code": os.getenv("TTS_LANGUAGE_CODE", "en-US"),
        "voice_name": os.getenv("TTS_VOICE_NAME", "en-US-Wavenet-D"),
        "speaking_rate": float(os.getenv("TTS_SPEAKING_RATE", "1.0")),
        "pitch": float(os.getenv("TTS_PITCH", "0.0"))
    }