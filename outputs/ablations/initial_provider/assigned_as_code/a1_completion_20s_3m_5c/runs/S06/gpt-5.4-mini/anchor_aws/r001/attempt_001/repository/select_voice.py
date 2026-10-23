from speech_client import get_client, get_config


def select_voice(payload=None, config=None):
    cfg = get_config(config)
    payload = dict(payload or {})
    client = get_client(cfg)
    voices = client.describe_voices(LanguageCode=payload.get("locale")) if payload.get("locale") else client.describe_voices()
    selected = None
    target = payload.get("voice_id")
    if target:
        for voice in voices.get("Voices", []):
            if voice.get("Id") == target:
                selected = voice
                break
    return {"voices": voices.get("Voices", []), "selected_voice": selected}
