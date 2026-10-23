from __future__ import annotations

from translation_client import get_client


def localized_audio_preview(text: str, voice: str = "Joanna"):
    client = get_client()
    return client.generate_audio_preview(text, voice=voice)
