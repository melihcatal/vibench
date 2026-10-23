from speech_client import get_tts_client


def list_voices(locale: str) -> list[dict]:
    client = get_tts_client()
    response = client.list_voices(language_code=locale)
    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else None,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voices


def select_voice(locale: str, gender_preference: str = "FEMALE") -> str:
    voices = list_voices(locale)
    for voice in voices:
        if voice["ssml_gender"] == gender_preference:
            return voice["name"]
    return voices[0]["name"] if voices else None
