import os
from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import Voice, VoiceSelectionResponse


def select_voice(language_code: str = None) -> VoiceSelectionResponse:
    """
    Lists or selects a voice for a target locale using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = get_tts_client()

    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            )
        )

    return VoiceSelectionResponse(voices=voices)
