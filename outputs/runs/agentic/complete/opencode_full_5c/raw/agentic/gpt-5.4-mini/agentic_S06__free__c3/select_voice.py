from speech_client import load_config


def select_voice(locale: str, preferred: str | None = None) -> str:
    config = load_config()
    catalog = {
        "en-US": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        "en-GB": ["fable", "shimmer", "alloy"],
        "es-ES": ["nova", "alloy"],
        "fr-FR": ["shimmer", "nova"],
    }
    voices = catalog.get(locale, [config.default_voice])
    if preferred in voices:
        return preferred
    return voices[0]
