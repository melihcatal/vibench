from speech_client import get_tts_client, get_default_voice
from speech_models import SsmlRequest, AudioResponse, normalize_ssml


def synthesize_ssml(ssml: str, voice: str | None = None, locale: str | None = None) -> bytes:
    client = get_tts_client()
    selected_voice = voice or get_default_voice(locale)
    request = SsmlRequest(ssml=normalize_ssml(ssml), voice=selected_voice, locale=locale)
    response = client.synthesize_ssml(request)
    if isinstance(response, AudioResponse):
        return response.audio_bytes
    if isinstance(response, bytes):
        return response
    raise TypeError('Unexpected response type from TTS provider')
