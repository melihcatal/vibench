# [SAME-SCENARIO] select_voice.py
# Lists or selects a voice for a target locale using ElevenLabs Text-to-Speech

import os
import requests
import json

# ---------- Configuration ----------
# Provider: ElevenLabs (identified by SDK import and API key)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1/voices"
# -----------------------------------


def list_voices(locale_filter: str = None) -> list[dict]:
    """Retrieve all voices and optionally filter by locale.

    Args:
        locale_filter (str, optional): Locale code such as 'en-us'.

    Returns:
        list[dict]: List of voice metadata dictionaries.
    """
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

    params = {}
    if locale_filter:
        params["search"] = locale_filter
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    response = requests.get(BASE_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def select_voice(locale_filter: str = None) -> dict:
    """Select a single voice that matches the locale (returns first match).

    Args:
        locale_filter (str, optional): Locale code such as 'en-us'.

    Returns:
        dict: Selected voice information.
    """
    voices = list_voices(locale_filter)
    if not voices:
        raise ValueError("No voices found")
    return voices[0]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     voice = select_voice("en-us")
#     print("Selected voice:", voice["name"], voice["id"])
