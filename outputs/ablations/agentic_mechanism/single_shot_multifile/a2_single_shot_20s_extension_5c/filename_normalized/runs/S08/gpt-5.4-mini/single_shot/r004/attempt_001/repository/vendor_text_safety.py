from typing import Optional
from openai import OpenAI
from document_client import get_openai_client

SAFETY_MODEL = "omni-moderation-latest"


def moderate_vendor_notes(text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(model=SAFETY_MODEL, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
