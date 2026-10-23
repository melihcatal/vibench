# [HELPER] speech_client.py
# Local configuration and client helper utilities for Text-to-Speech

import os
from typing import Dict, Any

# Azure TTS credentials (read from environment)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

# ElevenLabs credentials
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Simple helper to load env vars and validate required keys
REQUIRED_AZURE_VARS = ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]


def validate_azure_env() -> bool:
    missing = [v for v in REQUIRED_AZURE_VARS if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing Azure TTS environment variables: {missing}")
    return True


REQUIRED_ELEVEN_VARS = ["ELEVENLABS_API_KEY"]


def validate_eleven_env() -> bool:
    missing = [v for v in REQUIRED_ELEVEN_VARS if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing ElevenLabs environment variables: {missing}")
    return True


# Generic helper to get a configured client for a service
def get_azure_speech_client() -> Any:
    """Return a ready‑to‑use Azure Speech SDK client."""
    validate_azure_env()
    from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    return speech_config  # caller can create SpeechSynthesizer as needed


# Example usage within other modules
if __name__ == "__main__":
    client = get_azure_speech_client()
    print("Azure client configured:", client)  # just for demonstration
