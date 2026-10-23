# select_voice.py
import dashscope

# DashScope API key should be set in environment variable DASHSCOPE_API_KEY


def list_voices(locale: str = "en-us") -> list:
    """List available voices for a given locale using DashScope CosyVoice.

    Args:
        locale: Locale identifier (e.g., 'en-us').

    Returns:
        A list of voice info dictionaries.
    """
    client = dashscope.TextToSpeech()
    voices = client.list_voices(locale=locale)
    return voices


def select_voice(locale: str = "en-us", name_filter: str = None) -> dict:
    """Select a voice based on locale and optional name filter.

    Args:
        locale: Locale identifier.
        name_filter: Substring to match against voice names.

    Returns:
        The selected voice info dictionary, or None if no match.
    """
    voices = list_voices(locale)
    if not voices:
        return None
    if name_filter:
        matches = [v for v in voices if name_filter.lower() in v["name"].lower()]
        return matches[0] if matches else None
    return voices[0]
