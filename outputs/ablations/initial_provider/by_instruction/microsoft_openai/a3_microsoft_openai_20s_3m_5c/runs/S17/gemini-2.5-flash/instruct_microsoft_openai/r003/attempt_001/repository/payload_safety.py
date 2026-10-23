from security_client import SecurityClient
import os

def check_payload_safety(decrypted_text: str) -> dict:
    """Checks decrypted text payloads for unsafe content using OpenAI's moderation API."""
    security_client = SecurityClient("https://unused.vault.azure.net") # Placeholder URL, not used for OpenAI
    openai_client = security_client.get_openai_client()

    try:
        response = openai_client.moderations.create(input=decrypted_text)
        # The moderation response structure is a list of results, we usually care about the first one
        moderation_result = response.results[0]

        return {
            "flagged": moderation_result.flagged,
            "categories": {
                category.replace("_", " ").title(): value
                for category, value in moderation_result.categories.__dict__.items()
                if not category.startswith('_')
            },
            "category_scores": {
                category.replace("_", " ").title(): value
                for category, value in moderation_result.category_scores.__dict__.items()
                if not category.startswith('_')
            }
        }
    except Exception as e:
        return {"error": f"Error checking payload safety: {str(e)}"}

