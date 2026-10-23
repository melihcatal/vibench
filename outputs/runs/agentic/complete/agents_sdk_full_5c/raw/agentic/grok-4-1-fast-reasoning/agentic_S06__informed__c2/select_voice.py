from google.cloud import texttospeech
from speech_client import get_tts_client

def list_voices(locale: str = "en-US") -&gt; list[dict]:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=locale)
    return [
        {
            "name": voice.name,
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else None,
            "language_codes": voice.language_codes,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        for voice in response.voices
    ]

def select_voice(locale: str, gender: str | None = None) -&gt; str | None:
    """
    Selects a voice for a target locale, optionally filtering by gender.
    """
    voices = list_voices(locale)
    if gender:
        candidates = [v for v in voices if v["ssml_gender"] == gender.upper()]
    else:
        candidates = voices
    return candidates[0]["name"] if candidates else None
