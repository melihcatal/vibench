from typing import Any, Dict
from openai import OpenAI
from safety_client import get_openai_client

AUDIO_MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def reviewer_brief_audio(text: str, *, voice: str = VOICE, model: str | None = None) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    chosen_model = model or AUDIO_MODEL
    response = client.audio.speech.create(model=chosen_model, voice=voice, input=text)
    audio_bytes = response.read()
    return {"audio": audio_bytes, "voice": voice, "model": chosen_model}


if __name__ == "__main__":
    raise SystemExit(0)
