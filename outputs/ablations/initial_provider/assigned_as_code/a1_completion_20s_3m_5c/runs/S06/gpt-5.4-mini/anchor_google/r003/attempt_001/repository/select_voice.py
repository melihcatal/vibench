from google.cloud import texttospeech

from speech_client import get_tts_client


def select_voice(payload, config=None):
    config = config or {}
    client = get_tts_client()
    language_code = config.get("language_code") or payload.get("language_code") or "en-US"
    voices = client.list_voices(language_code=language_code).voices
    selected = None
    target_name = config.get("voice_name") or payload.get("voice_name")
    if target_name:
        for voice in voices:
            if voice.name == target_name:
                selected = voice
                break
    if selected is None:
        selected = voices[0] if voices else texttospeech.Voice(name="", language_codes=[language_code])
    return {"voice_name": selected.name, "language_codes": list(selected.language_codes)}
