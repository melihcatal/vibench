from speech_client import openai_client
from speech_models import ModerationResult

def moderate_text_openai(text_to_moderate: str) -> ModerationResult:
    """
    Moderates a transcript segment using OpenAI's Moderation API.

    Args:
        text_to_moderate: The text to be moderated.

    Returns:
        A ModerationResult object with the moderation outcome.
    """
    response = openai_client.moderations.create(
        input=text_to_moderate,
        model="text-moderation-latest" # Or "text-moderation-stable"
    )
    
    result = response.results[0]
    
    return ModerationResult(
        text=text_to_moderate,
        is_flagged=result.flagged,
        categories={cat: val for cat, val in result.categories.model_dump().items()}
    )
