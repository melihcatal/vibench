from google.cloud import texttospeech

from speech_client import get_client


def select_voice(target_locale: str):
    client = get_client()
    voices = client.list_voices(language_code=target_locale).voices
    return [
        {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
        }
        for voice in voices
    ]
