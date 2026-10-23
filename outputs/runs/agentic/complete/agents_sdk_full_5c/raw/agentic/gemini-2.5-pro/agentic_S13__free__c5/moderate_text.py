from safety_client import get_openai_client
from safety_models import ModerationRequest, ModerationResult

def moderate_text(request: ModerationRequest) -> ModerationResult:
    """
    Scores a single piece of text for unsafe content using OpenAI's Moderation API.

    Args:
        request: A ModerationRequest object containing the text to moderate.

    Returns:
        A ModerationResult object with the moderation outcome.
    """
    client = get_openai_client()
    
    response = client.moderations.create(
        input=request.text,
        model="text-moderation-latest" # Using the latest model from OpenAI
    )
    
    result = response.results[0]
    
    return ModerationResult(
        flagged=result.flagged,
        categories={cat: val for cat, val in result.categories.model_dump().items()},
        scores=result.category_scores.model_dump()
    )
