import os
from openai import OpenAI

def moderate_profile_text(text: str) -> dict:
    """
    Uses OpenAI's Moderation API to check for inappropriate content.
    Requires OPENAI_API_KEY environment variable.
    """
    if not text:
        return {"flagged": False, "categories": {}}

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.moderations.create(input=text)
        
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump()
        }
    except Exception as e:
        print(f"An error occurred with OpenAI moderation: {e}")
        # Fail safe: if moderation fails, flag the content for manual review.
        return {"flagged": True, "categories": {"moderation_error": True}}
