from google.cloud import texttospeech
from speech_client import get_speech_client
from speech_models import Voice


def list_voices(language_code: str = "en-US") -> list[Voice]:
    client = get_speech_client().tts_client
    voices = client.list_voices(language_code=language_code).voices
    return [
        Voice(
            name=v.name,
            language_codes=list(v.language_codes),
            gender=texttospeech.SsmlVoiceGender(v.ssml_gender).name,
            natural_sample_rate_hertz=v.natural_sample_rate_hertz,
        )
        for v in voices
    ]


def select_voice(language_code: str, gender: str = "NEUTRAL") -> Voice | None:
    voices = list_voices(language_code)
    for voice in voices:
        if voice.gender == gender.upper():
            return voice
    return None
