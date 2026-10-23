from speech_client import voice_catalog
from speech_models import voice_response


def select_voice(payload=None, config=None):
    payload = payload or {}
    locale = payload.get('locale') or (config or {}).get('locale')
    voices = voice_catalog(locale)
    target = payload.get('voice')
    if target:
        voices = [voice for voice in voices if voice['name'] == target]
    return voice_response(voices)
