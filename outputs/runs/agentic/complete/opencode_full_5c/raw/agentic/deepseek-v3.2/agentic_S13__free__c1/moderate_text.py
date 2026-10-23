import os
from typing import Dict, Any, Optional
from safety_client import SafetyClient


def moderate_text(text: str, categories: Optional[list] = None) -> Dict[str, Any]:
    """
    Score user text for unsafe or policy-violating content.

    Args:
        text: The text to moderate
        categories: Optional list of categories to check

    Returns:
        Dictionary with moderation results including scores and decisions
    """
    client = SafetyClient.get_client()

    # Use OpenAI's moderation API
    import openai

    response = openai.Moderation.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    # Extract category scores
    category_scores = {}
    for category, score in result.category_scores.items():
        category_scores[category] = score

    # Determine if flagged
    flagged = result.flagged

    # Get main categories
    main_categories = []
    for category, flagged_val in result.categories.items():
        if flagged_val:
            main_categories.append(category)

    return {
        "text": text,
        "flagged": flagged,
        "categories": main_categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": "text-moderation-latest",
    }
