from __future__ import annotations

from model_client import DEFAULT_MODERATION_MODEL, get_openai_client
from model_models import PromptSafetyResult


def check_prompt_safety(
    prompt_text: str, generated_text: str = ""
) -> PromptSafetyResult:
    client = get_openai_client()
    combined = (
        prompt_text
        if not generated_text
        else f"Prompt:\n{prompt_text}\n\nGenerated:\n{generated_text}"
    )
    response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=combined,
    )
    result = response.results[0]
    categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    scores = result.category_scores.model_dump()
    return PromptSafetyResult(
        provider="openai",
        model=DEFAULT_MODERATION_MODEL,
        is_safe=not result.flagged,
        categories=categories,
        scores=scores,
        flagged_segments=[combined] if result.flagged else [],
    )
