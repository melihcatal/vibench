import os

from openai import OpenAI


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    text = payload.get("text") or payload.get("vendor_notes") or ""
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0] if response.results else None
    return {"flagged": bool(result.flagged) if result else False, "categories": getattr(result, "categories", None)}
