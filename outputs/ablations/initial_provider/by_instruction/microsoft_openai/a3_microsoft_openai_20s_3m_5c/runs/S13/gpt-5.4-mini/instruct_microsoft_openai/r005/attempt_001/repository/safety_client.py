import os
from typing import Any, Dict, List

from openai import OpenAI

from safety_models import ModerationDecision, normalize_text


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_moderation_model() -> str:
    return os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_text_openai(text: str) -> ModerationDecision:
    client = get_client()
    model = get_moderation_model()
    response = client.moderations.create(model=model, input=normalize_text(text))
    result = response.results[0]
    return ModerationDecision(
        flagged=bool(result.flagged),
        categories=dict(result.categories),
        category_scores=dict(result.category_scores),
        provider="openai",
        raw=response.model_dump(),
    )


def moderate_batch_openai(texts: List[str]) -> List[ModerationDecision]:
    client = get_client()
    model = get_moderation_model()
    response = client.moderations.create(model=model, input=[normalize_text(text) for text in texts])
    return [
        ModerationDecision(
            flagged=bool(item.flagged),
            categories=dict(item.categories),
            category_scores=dict(item.category_scores),
            provider="openai",
            raw=response.model_dump(),
        )
        for item in response.results
    ]
