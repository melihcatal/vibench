from google.cloud import texttospeech
from speech_client import get_speech_client
from speech_models import VoicesResponse, Voice


def select_voice(language_code: str = "en-US"):
    """
    Lists the available voices for a given language code.

    Args:
        language_code (str): The language code to filter voices by (e.g., "en-US").

    Returns:
        A list of voice objects.
    """
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                language_codes=list(voice.language_codes),
                name=voice.name,
                ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
            )
        )
    return VoicesResponse(voices=voices)
