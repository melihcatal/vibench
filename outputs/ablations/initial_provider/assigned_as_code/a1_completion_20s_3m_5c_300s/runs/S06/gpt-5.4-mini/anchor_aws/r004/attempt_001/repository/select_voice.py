import boto3

from speech_client import load_config


def select_voice(payload=None, config=None):
    cfg = load_config(config)
    payload = payload or {}
    client = boto3.client("polly", region_name=cfg.region)
    voices = client.describe_voices(LanguageCode=payload.get("language_code"), Engine=payload.get("engine"))
    voice_list = voices.get("Voices", [])
    target_locale = payload.get("locale") or payload.get("language_code")
    if target_locale:
        filtered = [voice for voice in voice_list if target_locale.lower() in (voice.get("LanguageCode", "").lower(), voice.get("Id", "").lower())]
        if filtered:
            voice_list = filtered
    selected = payload.get("voice_id")
    if selected:
        for voice in voice_list:
            if voice.get("Id") == selected:
                return {"voices": voice_list, "selected_voice": voice}
    return {"voices": voice_list, "selected_voice": voice_list[0] if voice_list else None}
