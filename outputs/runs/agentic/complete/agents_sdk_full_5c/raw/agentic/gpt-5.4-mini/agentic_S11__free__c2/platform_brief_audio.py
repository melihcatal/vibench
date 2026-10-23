from typing import Dict

from openai import OpenAI

from model_client import get_openai_client, get_model_name


def platform_brief_audio(text: str) -> Dict[str, object]:
    client: OpenAI = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
    return {
        "provider": "openai",
        "model": model,
        "audio": speech,
    }
