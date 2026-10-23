from google.cloud import texttospeech

from speech_client import get_client, normalize_language_code


def select_voice(payload, config=None):
    payload = dict(payload or {})
    config = dict(config or {})
    client = get_client()
    voices = client.list_voices(language_code=normalize_language_code(payload.get("language_code", config.get("language_code"))))
    if payload.get("voice_name"):
        for voice in voices.voices:
            if voice.name == payload["voice_name"]:
                return {"voice_name": voice.name, "language_codes": list(voice.language_codes), "natural_sample_rate_hertz": voice.natural_sample_rate_hertz}
    voice = voices.voices[0] if voices.voices else texttospeech.Voice()
    return {"voice_name": getattr(voice, "name", ""), "language_codes": list(getattr(voice, "language_codes", [])), "natural_sample_rate_hertz": getattr(voice, "natural_sample_rate_hertz", 0)}
