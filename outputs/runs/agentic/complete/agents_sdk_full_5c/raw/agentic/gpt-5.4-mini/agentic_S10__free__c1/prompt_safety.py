from __future__ import annotations

from model_client import get_model_name, get_openai_client
from model_models import SafetyResult

PROVIDER = "openai"
MODEL_FAMILY = "omni-moderation-latest"


def prompt_safety(text: str) -> SafetyResult:
    client = get_openai_client()
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    result = moderation.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    explanation = ", ".join(categories) if categories else "No unsafe content detected."
    return SafetyResult(safe=not result.flagged, categories=categories, explanation=explanation)
