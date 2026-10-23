from google.cloud import texttospeech

from speech_client import client, load_config


def select_voice(payload, config=None):
    config = load_config(config)
    voices = client().list_voices(language_code=payload.get("locale", config.get("language_code")))
    items = []
    for voice in voices.voices:
        items.append({"name": voice.name, "language_codes": list(voice.language_codes), "ssml_gender": voice.ssml_gender.name})
    if payload.get("voice_name"):
        for item in items:
            if item["name"] == payload["voice_name"]:
                return {"voice": item, "voices": items}
    return {"voices": items}
