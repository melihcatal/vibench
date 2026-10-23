from speech_client import get_text_to_speech_client
from speech_models import VoiceSelection, Voice
from google.cloud import texttospeech


def select_voice(language_code: str, ssml_gender: str = None) -> list[Voice]:
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=language_code).voices

    filtered_voices = []
    for voice in voices:
        if ssml_gender and voice.ssml_gender.name != ssml_gender.upper():
            continue
        filtered_voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=voice.ssml_gender.name,
                natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
            )
        )
    return filtered_voices
