from security_client import get_openai_client

def check_payload_safety_openai(text_payload: str) -> dict:
    """
    Uses OpenAI's moderation endpoint to check for unsafe content.

    Args:
        text_payload: The decrypted text to check.

    Returns:
        A dictionary containing the moderation results.
    """
    client = get_openai_client()
    try:
        # Provider-specific call to OpenAI's Moderation API
        response = client.moderations.create(
            input=text_payload,
            model="text-moderation-stable"
        )
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump()
        }
    except Exception as e:
        return {"error": str(e)}
