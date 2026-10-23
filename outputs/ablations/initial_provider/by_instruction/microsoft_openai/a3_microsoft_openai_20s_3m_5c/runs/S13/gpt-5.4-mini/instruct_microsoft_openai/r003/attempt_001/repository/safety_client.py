import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from safety_models import ModerationDecision, normalize_text, normalize_texts


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderation_model() -> str:
    return os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def threshold_value(default: float = 0.5) -> float:
    raw = os.getenv("SAFETY_THRESHOLD")
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def moderate_text_request(text: str) -> ModerationDecision:
    client = get_client()
    response = client.moderations.create(model=moderation_model(), input=normalize_text(text))
    result = response.results[0]
    return ModerationDecision(
        flagged=bool(result.flagged),
        categories=dict(result.categories),
        category_scores=dict(result.category_scores),
        raw=response.model_dump(),
    )


def moderate_batch_request(texts: List[str]) -> List[ModerationDecision]:
    client = get_client()
    response = client.moderations.create(model=moderation_model(), input=normalize_texts(texts))
    decisions: List[ModerationDecision] = []
    for result in response.results:
        decisions.append(
            ModerationDecision(
                flagged=bool(result.flagged),
                categories=dict(result.categories),
                category_scores=dict(result.category_scores),
                raw=response.model_dump(),
            )
        )
    return decisions


def provider_name() -> str:
    return "openai"
