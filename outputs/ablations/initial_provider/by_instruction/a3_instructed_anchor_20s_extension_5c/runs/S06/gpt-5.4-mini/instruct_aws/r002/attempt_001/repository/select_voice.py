from speech_client import get_default_voice_map, get_polly_client


def list_voices(locale: str | None = None):
    client = get_polly_client()
    params = {}
    if locale:
        params["LanguageCode"] = locale
    response = client.describe_voices(**params)
    return response.get("Voices", [])


def select_voice(locale: str, preferred_gender: str | None = None):
    voices = list_voices(locale)
    if voices:
        if preferred_gender:
            for voice in voices:
                if voice.get("Gender", "").lower() == preferred_gender.lower():
                    return voice
        return voices[0]
    fallback = get_default_voice_map().get(locale, ["Joanna"])
    return {"Id": fallback[0], "LanguageCode": locale}
