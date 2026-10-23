from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def platform_brief_audio(text: str) -> bytes:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=normalize_text(text),
    )
    return speech.read()
