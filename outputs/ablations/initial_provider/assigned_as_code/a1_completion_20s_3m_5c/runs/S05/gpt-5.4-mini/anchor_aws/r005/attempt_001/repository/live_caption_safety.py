import os

from openai import OpenAI

from speech_models import normalize_text


def live_caption_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    text = normalize_text(payload.get("text"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"text": text, "unsafe": bool(result.flagged), "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)}
