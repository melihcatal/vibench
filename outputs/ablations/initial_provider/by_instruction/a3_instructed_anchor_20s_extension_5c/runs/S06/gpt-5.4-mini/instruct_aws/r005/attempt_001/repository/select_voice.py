import speech_client


def list_voices(locale: str | None = None):
    voices = speech_client.supported_voices()
    if not locale:
        return voices
    return [v for v in voices if v.get("LanguageCode") == locale or v.get("LanguageName", "").lower().startswith(locale.lower())]


def select_voice(locale: str) -> str:
    voices = list_voices(locale)
    if voices:
        return voices[0]["Id"]
    return speech_client.tts_voice(locale)
