from translation_client import get_openai_client
from typing import Dict, Any


def check_unsafe_content(text: str) -> Dict[str, Any]:
    """
    Checks for unsafe content using OpenAI's Moderation API.

    Args:
        text: The text to check.

    Returns:
        A dictionary indicating if the content is unsafe and which categories were flagged.
    """
    client = get_openai_client()
    response = client.moderations.create(input=text)

    result = response.results[0]

    is_flagged = result.flagged
    flagged_categories = [
        category for category, flagged in result.categories if flagged
    ]

    return {"is_unsafe": is_flagged, "flags": flagged_categories}
