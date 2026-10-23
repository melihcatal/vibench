import os
from typing import Any, Dict, Optional

from openai import OpenAI


def generate_spoken_briefing(platform_output: str, voice: str = "alloy", model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_model = model or os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    response = client.audio.speech.create(model=speech_model, voice=voice, input=platform_output)
    audio_bytes = getattr(response, "content", None)
    return {
        "provider": "openai",
        "model": speech_model,
        "voice": voice,
        "audio": audio_bytes,
        "response": response,
    }
