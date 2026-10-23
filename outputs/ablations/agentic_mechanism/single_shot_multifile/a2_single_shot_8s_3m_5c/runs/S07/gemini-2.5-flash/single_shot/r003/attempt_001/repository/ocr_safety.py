import os

from document_client import get_openai_client
from document_models import SafetyCheckInput, SafetyCheckOutput

def check_text_safety(
    safety_input: SafetyCheckInput,
) -> SafetyCheckOutput:
    """Checks extracted document text for unsafe content using OpenAI Moderation API."""
    client = get_openai_client()

    response = client.moderations.create(input=safety_input.text)
    moderation_result = response.results[0]

    return SafetyCheckOutput(
        unsafe=moderation_result.flagged,
        categories=moderation_result.categories.model_dump(),
        category_scores=moderation_result.category_scores.model_dump()
    )
