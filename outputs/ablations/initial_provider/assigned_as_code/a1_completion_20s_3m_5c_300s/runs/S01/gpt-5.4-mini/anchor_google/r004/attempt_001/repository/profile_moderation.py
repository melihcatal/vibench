from openai import OpenAI

from identity_models import normalize_text


def profile_moderation(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    text = normalize_text(payload.get("profile_text"))
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    result = moderation.results[0]
    return {"profile_text": text, "flagged": result.flagged, "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)}
