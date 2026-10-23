from google.cloud import texttospeech_v1 as tts
import os

def get_speech_client() -> tts.TextToSpeechClient:
    """
    Provides a configured Google Cloud Text-to-Speech client.
    """
    return tts.TextToSpeechClient()

def get_default_voice() -> str:
    """
    Returns the default voice name from environment or a fallback.
    """
    return os.getenv("TTS_DEFAULT_VOICE", "en-US-Studio-O")