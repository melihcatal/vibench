from speech_client import get_client, load_config


def select_voice(payload=None, config=None):
    cfg = load_config(config)
    client = get_client(cfg)
    voices = client.describe_voices(LanguageCode=cfg.get("language_code")).get("Voices", [])
    locale = (payload or {}).get("locale") if isinstance(payload, dict) else None
    if locale:
        for voice in voices:
            if voice.get("LanguageCode") == locale or locale in voice.get("LanguageCode", ""):
                return {"voice": voice, "voices": voices}
    voice_id = cfg.get("voice_id")
    if voice_id:
        for voice in voices:
            if voice.get("Id") == voice_id:
                return {"voice": voice, "voices": voices}
    return {"voice": voices[0] if voices else None, "voices": voices}
