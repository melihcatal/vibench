from google.cloud import texttospeech_v1 as tts
import os

def get_speech_client() -> tts.TextToSpeechClient:
    return tts.TextToSpeechClient()

def get_default_voice() -> str:
    return os.getenv("TTS_DEFAULT_VOICE", "en-US-Standard-A")

def get_default_language() -> str:
    return os.getenv("TTS_DEFAULT_LANGUAGE", "en-US")