from speech_client import create_polly_client


def select_voice(locale: str | None = None) -> list[dict]:
    client = create_polly_client()
    voices = client.describe_voices().get("Voices", [])
    if locale:
        wanted = locale.lower()
        voices = [voice for voice in voices if wanted in [voice.get("LanguageCode", "").lower(), voice.get("SupportedEngines", [""])[0].lower()]]
    return voices
