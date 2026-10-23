from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name

MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def reviewer_brief_audio(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    speech = client.audio.speech.create(model=MODEL, voice=VOICE, input=text)
    audio_bytes = getattr(speech, "content", None)
    if audio_bytes is None and hasattr(speech, "read"):
        audio_bytes = speech.read()
    return {
        "provider": provider_name(),
        "operation": "reviewer_brief_audio",
        "model": MODEL,
        "voice": VOICE,
        "text": text,
        "audio": audio_bytes,
        "metadata": metadata or {},
    }
