import os
from typing import Dict, Any, List
from openai import OpenAI


def platform_output_safety(text: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Check platform model output for unsafe content using OpenAI's moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Use OpenAI's moderation endpoint to check for unsafe content
    moderation_response = client.moderations.create(
        input=text, model="text-moderation-latest"
    )

    result = moderation_response.results[0]

    # Extract safety categories and flags
    categories = result.categories
    category_scores = result.category_scores

    # Determine if any category is flagged
    is_flagged = result.flagged

    # Get detailed category information
    flagged_categories = []
    for category_name, is_flagged_category in categories.__dict__.items():
        if is_flagged_category:
            flagged_categories.append(category_name)

    # Calculate overall safety score (lower is safer)
    safety_score = sum(
        [getattr(category_scores, cat) for cat in categories.__dict__.keys()]
    ) / len(categories.__dict__.keys())

    safety_report = {
        "text": text,
        "is_flagged": is_flagged,
        "flagged_categories": flagged_categories,
        "safety_score": safety_score,
        "category_scores": {
            cat: getattr(category_scores, cat) for cat in categories.__dict__.keys()
        },
        "moderation_model": moderation_response.model,
        "moderation_id": moderation_response.id,
    }

    return safety_report
