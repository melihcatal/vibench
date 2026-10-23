import os
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient


def get_elevenlabs_client():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    client = ElevenLabs(api_key=api_key)
    return client


def get_voice_id(client, voice_name=None, locale=None):
    voices = client.voices.get_all()
    voice_list = voices.voices if voices.voices else []
    if voice_name:
        for v in voice_list:
            if v.name.lower() == voice_name.lower():
                return v.voice_id
    if locale:
        locale_lower = locale.lower()
        for v in voice_list:
            labels = v.labels or {}
            accent = labels.get("accent", "").lower()
            language = labels.get("language", "").lower()
            description = labels.get("description", "").lower()
            if (
                locale_lower in accent
                or locale_lower in language
                or locale_lower in description
            ):
                return v.voice_id
    if voice_list:
        return voice_list[0].voice_id
    return None


def normalize_voice_info(voice):
    return {
        "voice_id": voice.voice_id,
        "name": voice.name,
        "category": voice.category,
        "labels": dict(voice.labels) if voice.labels else {},
        "preview_url": voice.preview_url,
    }


def list_all_voices(client):
    voices = client.voices.get_all()
    return [normalize_voice_info(v) for v in (voices.voices or [])]
