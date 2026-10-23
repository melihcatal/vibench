from security_client import get_openai_client
from security_models import ContentSafetyPayload


def check_content_safety(payload: ContentSafetyPayload) -> dict:
    openai_client = get_openai_client()

    try:
        response = openai_client.moderations.create(
            input=payload.text_content, model="text-moderation-latest"
        )

        result = response.results[0]

        flagged_categories = {
            cat: val for cat, val in result.categories.__dict__.items() if val
        }

        return {
            "is_safe": not result.flagged,
            "categories": flagged_categories,
        }
    except Exception as e:
        return {"is_safe": False, "error": str(e)}
