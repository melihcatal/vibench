from typing import List, Dict, Optional
import os
import dashscope
from dashscope.audio.tts import CosyVoice
from dashscope.common.api_identity import ApiIdentity


def initialize_client() -> CosyVoice:
    """Initialize the DashScope CosyVoice client with API key from environment."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    identity = ApiIdentity(api_key=api_key)
    dashscope.api_identity = identity
    return CosyVoice()


def list_voices(locale: Optional[str] = None) -> List[Dict[str, Any]]:
    """List available voices for a target locale using DashScope CosyVoice."""
    client = initialize_client()

    response = client.voices.list()
    if response.status_code != 200:
        raise RuntimeError(f"Failed to list voices: {response.message}")

    voices = response.output
    if locale:
        voices = [v for v in voices if v.get("locale", "").startswith(locale)]

    return voices


def select_voice(locale: str, gender: Optional[str] = None) -> Dict[str, Any]:
    """Select a voice for a target locale using DashScope CosyVoice."""
    voices = list_voices(locale)

    if gender:
        voices = [v for v in voices if v.get("gender", "").lower() == gender.lower()]

    if not voices:
        raise ValueError(f"No voices found for locale {locale} and gender {gender}")

    return voices[0]
