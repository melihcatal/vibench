from speech_client import list_voices


def select_voice(language_code: str | None = None) -> list[str]:
    return list_voices(language_code)
