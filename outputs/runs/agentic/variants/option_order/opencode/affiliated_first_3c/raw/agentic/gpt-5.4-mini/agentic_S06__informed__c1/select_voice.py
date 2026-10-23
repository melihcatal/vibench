from speech_client import list_supported_voices, voice_name_for_locale


def select_voice(locale: str, preferred: str = None):
    voices = list_supported_voices(locale)
    if preferred and preferred in voices:
        return preferred
    return voice_name_for_locale(locale)
