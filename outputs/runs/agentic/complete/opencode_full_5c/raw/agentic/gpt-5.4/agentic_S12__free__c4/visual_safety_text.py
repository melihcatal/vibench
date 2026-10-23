from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from vision_models import VisualSafetyTextResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def visual_safety_text(labels: Iterable[str]) -> VisualSafetyTextResult:
    client = OpenAI()
    text = ", ".join(label for label in labels if label)
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    return VisualSafetyTextResult(
        provider="openai", flagged=result.flagged, categories=categories
    )
