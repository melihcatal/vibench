from observability_client import get_openai_client
from typing import Dict, Any

def check_log_text_safety(text: str) -> Dict[str, Any]:
    openai_client = get_openai_client()

    response = openai_client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )

    moderation_result = response.results[0]
    # Convert pydantic models to dict for a plain Python dict return
    return {
        "flagged": moderation_result.flagged,
        "categories": {
            category: getattr(moderation_result.categories, category) for category in moderation_result.categories.__annotations__
        },
        "category_scores": {
            category: getattr(moderation_result.category_scores, category) for category in moderation_result.category_scores.__annotations__
        }
    }
