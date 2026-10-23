import os
from dashscope import Tts


def list_voices(locale: str) -> list[str]:
    """List available voices for a given locale using DashScope TTS.

    Returns a list of voice identifiers (e.g., 'cosy_1').
    """
    client = Tts(api_key=os.getenv("DASHSCOPE_API_KEY"))
    # Query the TTS API for voice catalogue; the real API returns a list of entries.
    # Here we call the generic REST endpoint to fetch metadata.
    payload = {
        "locale": locale,
    }
    response = client.metadata_voices(payload)
    # Assume response format contains a list of voice IDs under response["voices"]
    return [voice["id"] for voice in response["voices"]]


def select_voice(locale: str, preferred: str | None = None) -> str:
    """Select a voice identifier for a locale.

    If preferred is provided and matches an available voice, return it.
    Otherwise, return the first voice from the list.
    """
    voices = list_voices(locale)
    if preferred and preferred in voices:
        return preferred
    return voices[0] if voices else "default_voice"
