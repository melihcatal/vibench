from openai import OpenAI

from safety_client import get_openai_client, get_moderation_model
from safety_models import redact_text_with_categories


client: OpenAI = get_openai_client()
MODEL_ID = get_moderation_model()


def redact_unsafe(text: str) -> dict:
    response = client.moderations.create(model=MODEL_ID, input=text)
    result = response.results[0]
    categories = getattr(result, "categories", {})
    return {
        "original_text": text,
        "redacted_text": redact_text_with_categories(text, categories),
        "flagged": bool(getattr(result, "flagged", False)),
        "categories": categories,
    }
