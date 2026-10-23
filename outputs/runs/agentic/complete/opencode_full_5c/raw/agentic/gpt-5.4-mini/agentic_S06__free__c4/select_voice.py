from speech_models import VoiceSelection, normalize_locale


VOICES = [
    VoiceSelection("alloy", "en-us", "neutral"),
    VoiceSelection("echo", "en-us", "bright"),
    VoiceSelection("nova", "en-gb", "clear"),
    VoiceSelection("shimmer", "fr-fr", "warm"),
]


def list_voices(locale=None):
    if locale is None:
        return VOICES
    wanted = normalize_locale(locale)
    return [voice for voice in VOICES if voice.locale.startswith(wanted.split("-")[0])]


def select_voice(locale, preferred=None):
    voices = list_voices(locale)
    if preferred:
        for voice in voices:
            if voice.name == preferred:
                return voice
    return voices[0] if voices else VOICES[0]
