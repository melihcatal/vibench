from speech_client import client, load_config
from speech_models import voice_result


def select_voice(payload=None, config=None):
    payload = payload or {}
    cfg = load_config(config)
    polly = client(cfg)
    response = polly.describe_voices(LanguageCode=payload.get("locale") or payload.get("language_code"))
    voices = response.get("Voices", [])
    target = payload.get("voice_id")
    if target:
        voices = [voice for voice in voices if voice.get("Id") == target]
    return voice_result(voices)
