import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


class VendorTextSafetyError(Exception):
    pass


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise VendorTextSafetyError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def moderate_vendor_text(text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    if text is None:
        raise VendorTextSafetyError("text is required")
    client = _client()
    moderation = client.moderations.create(input=text)
    result = moderation.results[0]
    categories = dict(result.categories)
    category_scores = dict(result.category_scores)
    return {
        "provider": "openai",
        "model": model,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "text": text,
    }


def is_vendor_text_safe(text: str, threshold: float = 0.5) -> bool:
    report = moderate_vendor_text(text)
    if report["flagged"]:
        return False
    return all(score < threshold for score in report["category_scores"].values())
