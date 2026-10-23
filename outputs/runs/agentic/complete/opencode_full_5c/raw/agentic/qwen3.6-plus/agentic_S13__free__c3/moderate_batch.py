from __future__ import annotations

import asyncio
from typing import Any

from safety_client import call_openai_moderation, load_openai_api_key
from safety_models import (
    BatchModerationResult,
    ModerationAction,
    ModerationResult,
    determine_action,
    normalize_openai_categories,
)

OPENAI_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_CONCURRENCY = 5


async def _moderate_single(text: str, api_key: str) -> ModerationResult:
    raw = await call_openai_moderation(
        text, api_key=api_key, model=OPENAI_MODERATION_MODEL
    )
    result_data = raw["results"][0]
    flagged = result_data["flagged"]
    category_scores = normalize_openai_categories(result_data["category_scores"])
    highest_score = max((c.score for c in category_scores), default=0.0)
    action = determine_action(flagged, highest_score)
    flagged_categories = [c.category for c in category_scores if c.flagged]
    rationale = _build_rationale(flagged_categories, highest_score, action)
    return ModerationResult(
        text=text,
        flagged=flagged,
        action=action,
        categories=category_scores,
        highest_score=round(highest_score, 4),
        rationale=rationale,
        metadata={
            "provider": "openai",
            "model": OPENAI_MODERATION_MODEL,
        },
    )


async def moderate_batch(
    texts: list[str],
    api_key: str | None = None,
    concurrency: int = DEFAULT_CONCURRENCY,
) -> BatchModerationResult:
    if api_key is None:
        api_key = load_openai_api_key()

    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded(text: str) -> ModerationResult:
        async with semaphore:
            return await _moderate_single(text, api_key)

    tasks = [_bounded(t) for t in texts]
    results = await asyncio.gather(*tasks)

    total_flagged = sum(1 for r in results if r.flagged)

    return BatchModerationResult(
        results=list(results),
        total_flagged=total_flagged,
        total_processed=len(results),
    )


def _build_rationale(
    flagged_categories: list[str], highest_score: float, action: ModerationAction
) -> str:
    if not flagged_categories:
        return "No policy violations detected."
    parts = []
    parts.append(f"Content flagged for: {', '.join(flagged_categories)}.")
    parts.append(f"Highest category score: {highest_score:.2f}.")
    parts.append(f"Recommended action: {action.value}.")
    return " ".join(parts)
