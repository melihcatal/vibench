from typing import List, Optional

from azure.cognitiveservices import speech as speechsdk

from speech_client import create_speech_config, normalize_voice_name


DEFAULT_VOICES = [
    {"name": "en-US-JennyNeural", "locale": "en-US", "gender": "Female"},
    {"name": "en-US-GuyNeural", "locale": "en-US", "gender": "Male"},
    {"name": "en-GB-SoniaNeural", "locale": "en-GB", "gender": "Female"},
    {"name": "es-ES-ElviraNeural", "locale": "es-ES", "gender": "Female"},
    {"name": "fr-FR-DeniseNeural", "locale": "fr-FR", "gender": "Female"},
]


def list_or_select_voice(locale: str, preferred_name: Optional[str] = None) -> List[dict]:
    _ = create_speech_config()
    voices = [v for v in DEFAULT_VOICES if v["locale"].lower().startswith(locale.lower())]
    if preferred_name:
        normalized = normalize_voice_name(locale, preferred_name) or preferred_name
        voices = [v for v in voices if v["name"] == normalized] or [{"name": normalized, "locale": locale, "gender": "Unknown"}]
    return voices


def get_best_voice(locale: str, preferred_name: Optional[str] = None) -> str:
    voices = list_or_select_voice(locale, preferred_name)
    if not voices:
        return normalize_voice_name(locale, preferred_name) or "en-US-JennyNeural"
    return voices[0]["name"]
