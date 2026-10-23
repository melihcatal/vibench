from speech_client import get_tts_client


def list_voices(language_codes: str | list[str] = "en-US") -> list[dict]:
    if isinstance(language_codes, str):
        language_codes = [language_codes]
    client = get_tts_client()
    response = client.list_voices(languages=language_codes)
    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else None,
                "language_codes": voice.language_codes,
            }
        )
    return voices


def select_voice(language_code: str, ssml_gender: str | None = None) -> str | None:
    voices = list_voices(language_code)
    if ssml_gender:
        filtered = [
            v
            for v in voices
            if v["ssml_gender"] and v["ssml_gender"].lower() == ssml_gender.lower()
        ]
    else:
        filtered = voices
    return filtered[0]["name"] if filtered else None
