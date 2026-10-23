from google.cloud import texttospeech

from speech_client import tts_client
from speech_models import normalize_locale


def select_voice(target_locale):
    client = tts_client()
    voices = client.list_voices(language_code=normalize_locale(target_locale)).voices
    if not voices:
        return {"voices": [], "selected_voice": None}
    voice = voices[0]
    return {"voices": [v.name for v in voices], "selected_voice": voice.name}
