import os
import openai


def vendor_text_safety(text_to_moderate: str) -> dict:
    """
    Uses OpenAI's Moderation endpoint to check for unsafe content in vendor notes.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        response = openai.moderations.create(
            input=text_to_moderate, model="text-moderation-stable"
        )
        moderation_result = response.results[0]

        return {
            "flagged": moderation_result.flagged,
            "categories": dict(moderation_result.categories),
        }

    except Exception as e:
        # In a real app, log the error
        return {"error": str(e)}
