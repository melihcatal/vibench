from speech_client import get_client, load_config


def select_voice(payload=None, config=None):
    payload = payload or {}
    cfg = load_config(config)
    client = get_client(cfg)
    voices = client.describe_voices(LanguageCode=payload.get("locale") or cfg["language_code"])
    items = voices.get("Voices", [])
    if payload.get("voice_id"):
        for voice in items:
            if voice.get("Id") == payload["voice_id"]:
                return voice
    return items
