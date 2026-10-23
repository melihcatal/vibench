from speech_client import TextToSpeechClient
from speech_models import Voice, VoiceSelection

def select_voice(payload, config=None) -> list[Voice]:
    config = config or {}
    client = TextToSpeechClient()
    language_code = payload.get("language_code", config.get("language_code"))
    voices = client.list_voices(language_code=language_code)

    # Further filtering based on payload if needed (e.g., gender, specific name)
    filtered_voices = []
    for voice in voices:
        if "gender" in payload and voice.gender != payload["gender"].upper():
            continue
        if "name" in payload and voice.name != payload["name"]:
            continue
        filtered_voices.append(voice)

    return filtered_voices
