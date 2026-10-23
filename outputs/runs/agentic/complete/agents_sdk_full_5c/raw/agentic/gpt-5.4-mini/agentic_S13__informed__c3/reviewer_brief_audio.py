from __future__ import annotations

from safety_client import SafetyClient
from safety_models import AudioBriefRequest

TTS_MODEL = "azure-speech-tts"


def reviewer_brief_audio(text: str, voice: str = "en-US-AriaNeural") -> dict:
    client = SafetyClient()
    result = client.generate_brief_audio(AudioBriefRequest(text=text, voice=voice))
    return {"provider": "Azure AI Speech", "model": TTS_MODEL, **result}
