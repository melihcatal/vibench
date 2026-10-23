import os
from speech_client import get_tts_client

def list_voices(locale: str = "en-US") -> list[dict]:
    """Retrieve and return a list of available voices for the given locale.

    Args:
        locale: BCP-47 language tag (e.g., 'en-US', 'fr-FR').

    Returns:
        List of dicts with keys: 'Name', 'DisplayName', 'Gender', 'Locale'.
    """
    client = get_tts_client()
    voices = client.list_voices(locale=locale)
    return [
        {
            "Name": v.name,
            "DisplayName": v.display_name,
            "Gender": v.gender,
            "Locale": v.locale,
        }
        for v in voices
    ]

if __name__ == "__main__":
    voices_en_us = list_voices("en-US")
    print(f"Found {len(voices_en_us)} voices for en-US")
    for v in voices_en_us[:5]:
        print(v)
