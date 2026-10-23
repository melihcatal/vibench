from safety_client import get_openai_client, moderation_model
from safety_models import normalize_moderation_response


def redact_unsafe(text: str):
    client = get_openai_client()
    response = client.moderations.create(model=moderation_model(), input=text)
    result = normalize_moderation_response(response.model_dump())
    if not result.flagged:
        return {"text": text, "redacted": False, "categories": result.categories}
    return {"text": "[REDACTED]", "redacted": True, "categories": result.categories}
