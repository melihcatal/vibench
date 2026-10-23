from speech_client import get_tts_client
from speech_models import VoiceSelectionRequest, VoiceListResponse


def select_voice(locale: str | None = None, gender: str | None = None, name: str | None = None) -> str:
    client = get_tts_client()
    response = client.list_voices(VoiceSelectionRequest(locale=locale, gender=gender, name=name))
    if isinstance(response, VoiceListResponse):
        return response.pick_best().name
    if isinstance(response, list) and response:
        return response[0].get('name')
    raise ValueError('No matching voice found')
