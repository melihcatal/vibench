"""
Check narration scripts for unsafe content using the OpenAI Moderation API.
"""
from speech_client import get_openai_client
from speech_models import SafetyCheckResponse

def check_script_safety_openai(text: str) -> SafetyCheckResponse:
    """
    Checks a script for unsafe content using OpenAI's Moderation endpoint.

    Args:
        text: The script text to check.

    Returns:
        A SafetyCheckResponse object with the moderation result.
    """
    client = get_openai_client()

    response = client.moderations.create(
        input=text,
        model="text-moderation-latest" # or "text-moderation-stable"
    )

    result = response.results[0]
    
    return SafetyCheckResponse(
        is_flagged=result.flagged,
        details=result.categories.model_dump()
    )
