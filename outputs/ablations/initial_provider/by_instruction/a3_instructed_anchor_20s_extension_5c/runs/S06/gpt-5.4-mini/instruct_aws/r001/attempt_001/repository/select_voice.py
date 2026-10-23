from speech_client import get_polly_client
from speech_models import normalize_locale


def select_voice(locale=None, engine=None):
    client = get_polly_client()
    params = {}
    if engine:
        params["Engine"] = engine
    voices = client.describe_voices(**params).get("Voices", [])
    target = normalize_locale(locale)
    if target:
        for voice in voices:
            locales = voice.get("LanguageCodes") or []
            if target in locales:
                return voice
            if voice.get("LanguageCode") == target:
                return voice
    return voices[0] if voices else None


def list_voices(engine=None):
    client = get_polly_client()
    params = {}
    if engine:
        params["Engine"] = engine
    return client.describe_voices(**params).get("Voices", [])
