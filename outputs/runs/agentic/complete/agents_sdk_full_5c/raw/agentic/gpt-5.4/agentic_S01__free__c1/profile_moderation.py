from __future__ import annotations

from openai import OpenAI

from identity_models import ModerationResult


MODEL = "omni-moderation-latest"


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model=MODEL, input=profile_text)
    moderation = response.results[0]
    categories = moderation.categories.model_dump()
    result = ModerationResult(
        allowed=not moderation.flagged,
        flagged_categories={k: v for k, v in categories.items() if v},
    )
    payload = result.to_dict()
    payload["model"] = MODEL
    return payload
