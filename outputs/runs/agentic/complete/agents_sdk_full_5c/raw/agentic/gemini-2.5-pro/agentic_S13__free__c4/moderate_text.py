"""Scores user text for unsafe or policy-violating content using OpenAI."""
from safety_client import get_openai_client
from safety_models import ModerationResult


def moderate_text_openai(text_content: str) -> ModerationResult:
    """
    Scores a single string for unsafe content using the OpenAI Moderation API.

    Args:
        text_content: The text to moderate.

    Returns:
        A standardized moderation result.
    """
    client = get_openai_client()
    response = client.moderations.create(input=text_content)
    
    result = response.results[0]
    
    return ModerationResult(
        flagged=result.flagged,
        categories={cat: val for cat, val in result.categories},
        scores={cat: score for cat, score in result.category_scores.items()},
        details=f"OpenAI Moderation Model: {response.model}"
    )
