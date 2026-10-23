from __future__ import annotations

from typing import Iterable, List

from vision_client import OPENAI_MODERATION_MODEL, get_openai_client
from vision_models import TextSafetyResult


def visual_safety_text(labels: Iterable[str]) -> TextSafetyResult:
    label_list: List[str] = [label for label in labels if label]
    text = ", ".join(label_list)
    client = get_openai_client()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return TextSafetyResult(
        flagged=bool(result.flagged),
        categories=categories,
        model=OPENAI_MODERATION_MODEL,
        raw_response=response.model_dump(),
    )
