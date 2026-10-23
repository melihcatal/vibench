import os
from model_client import ManagedModelClient


def generate_brief_audio(text: str, voice: str = "alloy") -> bytes:
    # Concrete provider: Google Cloud Text-to-Speech
    client = ManagedModelClient(provider="google-tts")
    audio_bytes = client.text_to_speech(input_text=text, voice=voice)
    return audio_bytes
