from __future__ import annotations

from openai import OpenAI

from vision_models import UnsafeTextCheckResult


def visual_safety_text(text: str) -> UnsafeTextCheckResult:
    client = OpenAI(api_key=__import__("os").environ["OPENAI_API_KEY"])
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    raw = response.model_dump()
    result = raw["results"][0]
    categories = {
        name: bool(flag) for name, flag in result.get("categories", {}).items()
    }
    return UnsafeTextCheckResult(
        provider="openai",
        flagged=bool(result.get("flagged", False)),
        categories=categories,
        raw_response=raw,
    )
