from __future__ import annotations

from typing import Any, Dict

from model_client import DEFAULT_MODERATION_MODEL, get_openai_client
from model_models import ModerationResult


def check_prompt_safety(prompt: str, generated_text: str) -> Dict[str, ModerationResult]:
    client = get_openai_client()
    prompt_resp = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=prompt,
    )
    output_resp = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=generated_text,
    )

    def _convert(resp: Any) -> ModerationResult:
        result = resp.results[0]
        categories = result.categories
        if hasattr(categories, "model_dump"):
            categories = categories.model_dump()
        return ModerationResult(
            flagged=result.flagged,
            categories=categories,
            model=DEFAULT_MODERATION_MODEL,
        )

    return {
        "prompt": _convert(prompt_resp),
        "generated_text": _convert(output_resp),
    }
