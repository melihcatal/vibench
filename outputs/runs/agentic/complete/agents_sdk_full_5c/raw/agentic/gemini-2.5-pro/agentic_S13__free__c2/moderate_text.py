import os
from openai import OpenAI
from safety_models import ModerationResponse

def moderate_text(text_to_moderate: str) -> ModerationResponse:
    """
    Scores user text for unsafe or policy-violating content using OpenAI.

    Args:
        text_to_moderate: The text to moderate.

    Returns:
        A ModerationResponse object with the moderation decision.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(
        input=text_to_moderate,
        model="text-moderation-stable"
    )

    result = response.results[0]
    
    scores = {category: score for category, score in result.category_scores.__dict__.items()}

    return ModerationResponse(
        is_safe=not result.flagged,
        scores=scores,
        raw_response=result.model_dump()
    )
