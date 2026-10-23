from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client
from model_models import normalize_text


def platform_output_safety(text: str) -> dict:
    client: AzureOpenAI = get_client()
    moderation = client.moderations.create(input=normalize_text(text))
    result = moderation.results[0]
    return {
        "provider": "azure-openai",
        "flagged": bool(getattr(result, "flagged", False)),
        "categories": getattr(result, "categories", None),
        "category_scores": getattr(result, "category_scores", None),
    }
