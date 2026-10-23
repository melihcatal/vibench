import os
from openai import OpenAI

def check_visual_labels_safety(labels_text: str) -> dict:
    """
    Checks generated visual labels for unsafe text content using OpenAI Moderation API.

    Args:
        labels_text: A string containing the combined text of visual labels.

    Returns:
        A dictionary indicating if the text is flagged and detailed moderation categories.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.moderations.create(
        input=labels_text
    )
    
    moderation_result = response.results[0]
    
    return {
        'flagged': moderation_result.flagged,
        'categories': {
            category.replace("_", ""): value
            for category, value in moderation_result.categories.model_dump().items()
        },
        'category_scores': {
            category.replace("_", ""): value
            for category, value in moderation_result.category_scores.model_dump().items()
        }
    }
