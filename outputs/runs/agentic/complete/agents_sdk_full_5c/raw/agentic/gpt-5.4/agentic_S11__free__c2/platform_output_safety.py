from __future__ import annotations

from model_client import get_azure_openai_client, get_moderation_model
from model_models import SafetyResult



def platform_output_safety(text: str) -> SafetyResult:
    client = get_azure_openai_client()
    response = client.moderations.create(
        model=get_moderation_model(),
        input=text,
    )
    result = response.results[0]
    categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    return SafetyResult(
        safe=not bool(getattr(result, "flagged", False)),
        categories=categories,
        raw=response,
    )
