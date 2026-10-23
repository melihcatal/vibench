import os
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from model_client import get_llm_client
from model_models import normalize_model_response


def check_prompt_safety(prompt: str, model: Optional[str] = None) -> Dict[str, any]:
    """
    Check prompts for unsafe content using OpenAI's moderation API.

    Args:
        prompt: The prompt to check
        model: Optional specific model to use for checking

    Returns:
        Dictionary with safety results
    """
    client = get_llm_client()

    try:
        # Use OpenAI's moderation endpoint
        response = client.moderations.create(
            input=prompt, model="text-moderation-latest"
        )

        results = response.results[0]

        return {
            "flagged": results.flagged,
            "categories": {
                "hate": results.categories.hate,
                "hate_threatening": results.categories.hate_threatening,
                "self_harm": results.categories.self_harm,
                "sexual": results.categories.sexual,
                "sexual_minors": results.categories.sexual_minors,
                "violence": results.categories.violence,
                "violence_graphic": results.categories.violence_graphic,
            },
            "category_scores": {
                "hate": results.category_scores.hate,
                "hate_threatening": results.category_scores.hate_threatening,
                "self_harm": results.category_scores.self_harm,
                "sexual": results.category_scores.sexual,
                "sexual_minors": results.category_scores.sexual_minors,
                "violence": results.category_scores.violence,
                "violence_graphic": results.category_scores.violence_graphic,
            },
            "model_used": "text-moderation-latest",
            "provider": "openai",
        }

    except Exception as e:
        raise Exception(f"Failed to check prompt safety: {str(e)}")


def check_generated_text_safety(text: str) -> Dict[str, any]:
    """
    Check generated text for unsafe content.

    Args:
        text: The generated text to check

    Returns:
        Dictionary with safety results
    """
    return check_prompt_safety(text)


def get_safety_recommendations(safety_results: Dict[str, any]) -> List[str]:
    """
    Get safety recommendations based on moderation results.

    Args:
        safety_results: Results from safety check

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if safety_results.get("flagged", False):
        recommendations.append(
            "Content flagged as unsafe. Consider revising the prompt."
        )

        categories = safety_results.get("categories", {})
        for category, flagged in categories.items():
            if flagged:
                recommendations.append(
                    f"Content contains {category.replace('_', ' ')}."
                )

    if not recommendations:
        recommendations.append("Content appears safe for processing.")

    return recommendations


def filter_unsafe_content(
    text: str, threshold: float = 0.5
) -> Tuple[str, Dict[str, any]]:
    """
    Filter unsafe content from text based on safety scores.

    Args:
        text: Text to filter
        threshold: Score threshold for filtering (0.0 to 1.0)

    Returns:
        Tuple of (filtered_text, safety_analysis)
    """
    safety_results = check_generated_text_safety(text)

    filtered_text = text
    needs_filtering = False

    category_scores = safety_results.get("category_scores", {})
    for category, score in category_scores.items():
        if score > threshold:
            needs_filtering = True
            break

    if needs_filtering:
        # Simple filtering - replace with placeholder for high-risk content
        filtered_text = "[Content filtered for safety reasons]"

    return filtered_text, safety_results
