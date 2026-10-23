# [SAME-SCENARIO] select_voice.py
# Lists or selects a voice for a target locale using IBM Watson Text to Speech

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

# Local helper import
from speech_client import get_watson_client


def list_voices(locale: str = None) -> dict:
    """List available voices, optionally filtered by locale.

    Args:
        locale (str, optional): Locale code (e.g., 'en-US').

    Returns:
        dict: JSON payload with voice metadata.
    """
    client = get_watson_client()
    return client.list_voices().get_result()


def get_voice_by_locale(locale: str, gender: str = None) -> str:
    """Select a voice that matches a locale and optional gender.

    Args:
        locale (str): Locale code (e.g., 'en-US').
        gender (str, optional): 'male' or 'female'.

    Returns:
        str: Voice identifier or None if not found.
    """
    voices = list_voices(locale).get("voices", [])
    for voice in voices:
        if voice["language"] == locale:
            if gender and voice["gender"] != gender:
                continue
            return voice["name"]
    return None
