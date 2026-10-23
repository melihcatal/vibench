# [SAME-SCENARIO] select_voice.py
# Lists or selects a voice for a target locale using Google Cloud Text-to-Speech

from google.cloud import texttospeech


def list_voices(locale: str = "en-US") -> list[dict]:
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_codes=[locale]).voices
    return [
        {
            "name": v.name,
            "language_code": v.language_codes[0],
            "ssml_gender": v.ssml_gender,
            "natural_sample_rate_hertz": v.natural_sample_rate_hertz,
        }
        for v in voices
    ]


def select_voice(locale: str, name: str) -> dict:
    voices = list_voices(locale)
    for v in voices:
        if v["name"] == name:
            return v
    raise ValueError(f"Voice {name} not found for locale {locale}")
