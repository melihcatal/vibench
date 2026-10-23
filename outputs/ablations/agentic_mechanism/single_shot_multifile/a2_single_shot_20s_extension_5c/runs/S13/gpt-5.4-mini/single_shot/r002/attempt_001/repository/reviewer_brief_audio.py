from typing import Dict
from openai import OpenAI
from safety_client import get_openai_client

AUDIO_MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def reviewer_brief_audio(text: str, client: OpenAI = None) -> Dict[str, str]:
    client = client or get_openai_client()
    resp = client.audio.speech.create(model=AUDIO_MODEL, voice=VOICE, input=text)
    return {"audio_format": "mp3", "model": AUDIO_MODEL, "voice": VOICE, "content_type": getattr(resp, "content_type", "audio/mpeg")}
