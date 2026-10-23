from typing import Any, Dict

from openai import OpenAI

from document_client import load_document_settings
from document_models import coerce_text_payload


def vendor_text_safety(text: Any) -> Dict[str, Any]:
    settings = load_document_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=coerce_text_payload(text),
    )
    result = response.results[0] if response.results else None
    return {
        "flagged": bool(getattr(result, "flagged", False)),
        "categories": getattr(result, "categories", {}),
        "category_scores": getattr(result, "category_scores", {}),
    }
