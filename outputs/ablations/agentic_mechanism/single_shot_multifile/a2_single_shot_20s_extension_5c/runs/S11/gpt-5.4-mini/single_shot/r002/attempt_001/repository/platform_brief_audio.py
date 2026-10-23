from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client

SPEECH_MODEL = "gpt-4o-mini-tts"
VOICE_NAME = "alloy"


def generate_platform_brief_audio(text: str, client: OpenAI | None = None) -> Dict[str, Any]:
    api_client = client or get_openai_client()
    response = api_client.audio.speech.create(model=SPEECH_MODEL, voice=VOICE_NAME, input=text)
    return {"provider": "openai", "model": SPEECH_MODEL, "voice": VOICE_NAME, "raw": response}
