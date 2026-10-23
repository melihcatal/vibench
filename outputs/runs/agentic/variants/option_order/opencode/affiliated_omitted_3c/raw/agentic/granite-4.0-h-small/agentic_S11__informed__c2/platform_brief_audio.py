import os
from model_models import normalize_response, NormalizedOutput
from model_client import ManagedModelClient

# Concrete provider for TTS – Azure AI Speech TTS
TTS_PROVIDER: Literal["azure"] = "azure"

# Provider identifier used throughout the workflow
PROVIDER: Literal["huggingface"] = "huggingface"


def generate_brief_audio(
    raw_output: NormalizedOutput, voice_name: str = "arthur"
) -> bytes:
    """Create a short spoken briefing from provider output using Azure Speech TTS.

    The concrete TTS service is identified by the TTS_PROVIDER constant.
    Returns raw audio bytes (WAV format) for downstream use.
    """
    client = ManagedModelClient()
    text = raw_output["content"]
    # Simulated TTS SDK call (replace with azure.cognitiveservices.speech)
    audio_bytes = _fake_tts(text, voice_name)
    return audio_bytes


def _fake_tts(text: str, voice: str) -> bytes:
    # Placeholder – real implementation returns binary WAV audio
    # Here we encode the text as a simple "audio" marker
    return f"Audio for '{text}' in voice {voice}".encode("utf-8")
