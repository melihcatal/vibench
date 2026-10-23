from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import normalize_text


def reviewer_brief_audio(brief_text: str) -> bytes:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    speech = client.audio.speech.create(
        model=cfg.speech_model,
        voice="alloy",
        input=normalize_text(brief_text),
    )
    return speech.read()
