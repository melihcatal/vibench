from speech_client import build_polly_client, normalize_voice_name


def list_voices(locale_prefix: str = ""):
    client = build_polly_client()
    paginator = client.get_paginator("describe_voices")
    voices = []
    for page in paginator.paginate():
        for voice in page.get("Voices", []):
            if not locale_prefix or voice.get("LanguageCode", "").startswith(locale_prefix):
                voices.append(voice)
    return voices


def select_voice(locale_prefix: str, preferred_voice: str | None = None):
    preferred_voice = normalize_voice_name(preferred_voice)
    voices = list_voices(locale_prefix)
    if preferred_voice:
        for voice in voices:
            if voice.get("Id") == preferred_voice:
                return voice
    return voices[0] if voices else None
