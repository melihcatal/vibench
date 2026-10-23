from __future__ import annotations

from identity_client import load_config
from identity_models import ModerationResult, compact_categories

from openai import OpenAI


def profile_moderation(profile_text: str) -> ModerationResult:
    config = load_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=profile_text,
    )
    result = response.results[0]
    raw = result.model_dump()
    return ModerationResult(
        flagged=result.flagged,
        categories=compact_categories(raw),
        raw=raw,
    )
