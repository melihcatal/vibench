from __future__ import annotations

from openai import OpenAI

from identity_models import ModerationResult


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    moderation = result.results[0]
    flagged_categories = {name: bool(value) for name, value in moderation.categories.model_dump().items()}
    approved = not moderation.flagged
    return ModerationResult(approved=approved, flagged_categories=flagged_categories).__dict__
