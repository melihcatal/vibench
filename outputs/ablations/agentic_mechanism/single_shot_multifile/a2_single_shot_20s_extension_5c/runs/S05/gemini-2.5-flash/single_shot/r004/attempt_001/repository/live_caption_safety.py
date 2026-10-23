import os
from typing import Dict, Any
import openai

def check_safety(text: str) -> Dict[str, Any]:
    """Checks live transcript text for unsafe content using OpenAI Moderation API.

    Args:
        text: The transcript text to check.

    Returns:
        Dict[str, Any]: A dictionary containing moderation results.
            Example: {"flagged": bool, "categories": {...}, "category_scores": {...}}
    """
    if not text.strip():
        return {"flagged": False, "categories": {}, "category_scores": {}}

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.moderations.create(
            input=text,
            model="text-moderation-latest"
        )
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": {cat.id: cat.present for cat in result.categories},
            "category_scores": {cat.id: cat.score for cat in result.category_scores}
        }
    except Exception as e:
        print(f"OpenAI moderation error: {e}")
        return {"flagged": False, "error": str(e)}
