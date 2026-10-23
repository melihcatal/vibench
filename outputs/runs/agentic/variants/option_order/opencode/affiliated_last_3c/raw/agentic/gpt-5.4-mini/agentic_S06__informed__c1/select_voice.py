from speech_client import client, load_config


def list_voices(locale: str | None = None):
    polly = client(load_config())
    kwargs = {"Engine": load_config().engine}
    if locale:
        kwargs["LanguageCode"] = locale
    return polly.describe_voices(**kwargs).get("Voices", [])


def select_voice(locale: str, preference: str | None = None) -> str:
    voices = list_voices(locale)
    if preference:
        for voice in voices:
            if voice.get("Id") == preference:
                return preference
    return voices[0]["Id"] if voices else (load_config().default_voice or "Joanna")
