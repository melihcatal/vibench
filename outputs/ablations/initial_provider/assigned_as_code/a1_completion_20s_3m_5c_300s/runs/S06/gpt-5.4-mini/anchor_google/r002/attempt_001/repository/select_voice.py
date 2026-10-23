from google.cloud import texttospeech

from speech_client import get_tts_client
from speech_models import normalize_locale, voice_to_dict


def select_voice(payload, config=None):
    config = config or {}
    locale = normalize_locale(payload.get("locale") if isinstance(payload, dict) else payload)
    client = get_tts_client()
    voices = client.list_voices(language_code=locale).voices
    selected = None
    if isinstance(payload, dict) and payload.get("voice_name"):
        for voice in voices:
            if voice.name == payload["voice_name"]:
                selected = voice
                break
    if selected is None:
        selected = voices[0] if voices else texttospeech.Voice(name="", language_codes=[locale])
    return {"voices": [voice_to_dict(v) for v in voices], "selected_voice": voice_to_dict(selected)}
