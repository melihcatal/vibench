import os
from openai import OpenAI
from document_client import get_openai_client
from document_models import SafetyCheckRequest, SafetyCheckResponse, SafetyCategory


def ocr_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Check extracted document text for unsafe content using OpenAI Moderation API."""
    client = get_openai_client()

    response = client.moderations.create(
        model="text-moderation-latest", input=request.text
    )

    moderation_result = response.results[0]
    categories = []

    for (
        category_name,
        category_data,
    ) in moderation_result.categories.model_dump().items():
        if category_data.get("flagged", False):
            score = moderation_result.category_scores.get(category_name, 0.0)
            categories.append(
                SafetyCategory(category=category_name, score=score, flagged=True)
            )

    return SafetyCheckResponse(
        categories=categories,
        provider="openai",
        model_id="text-moderation-latest",
        raw_response=response,
    )
