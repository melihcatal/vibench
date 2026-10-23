import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_client
from model_models import TaskType


def check_prompt_safety(prompt: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using OpenAI's moderation API.

    Args:
        prompt: The prompt or text to check

    Returns:
        Dictionary with safety analysis results
    """
    client = get_client()

    try:
        # Use OpenAI's moderation endpoint
        response = client.moderations.create(
            input=prompt, model="text-moderation-latest"
        )

        moderation_result = response.results[0]

        # Extract categories and flags
        categories = moderation_result.categories
        category_scores = moderation_result.category_scores

        # Determine if any category is flagged
        is_flagged = moderation_result.flagged

        # Get specific flagged categories
        flagged_categories = [
            category
            for category, flagged in categories.__dict__.items()
            if flagged and not category.startswith("_")
        ]

        # Calculate overall safety score (lower is safer)
        safety_score = (
            sum([getattr(category_scores, cat) for cat in flagged_categories])
            if flagged_categories
            else 0.0
        )

        return {
            "is_safe": not is_flagged,
            "flagged_categories": flagged_categories,
            "safety_score": safety_score,
            "category_scores": {
                cat: getattr(category_scores, cat)
                for cat in [
                    "harassment",
                    "harassment_threatening",
                    "hate",
                    "hate_threatening",
                    "self_harm",
                    "self_harm_instructions",
                    "self_harm_intent",
                    "sexual",
                    "sexual_minors",
                    "violence",
                    "violence_graphic",
                ]
            },
            "model_used": "text-moderation-latest",
        }

    except Exception as e:
        raise Exception(f"Failed to check prompt safety: {str(e)}")


def check_generated_text_safety(text: str, original_prompt: str = "") -> Dict[str, Any]:
    """
    Check generated text for safety issues.

    Args:
        text: The generated text to check
        original_prompt: Original prompt for context

    Returns:
        Dictionary with safety analysis results
    """
    # Combine prompt and generated text for context
    full_text = (
        f"Prompt: {original_prompt}\n\nGenerated text: {text}"
        if original_prompt
        else text
    )

    return check_prompt_safety(full_text)


def get_safety_recommendations(safety_result: Dict[str, Any]) -> str:
    """
    Get safety recommendations based on moderation results.

    Args:
        safety_result: Result from check_prompt_safety

    Returns:
        Safety recommendations
    """
    if safety_result["is_safe"]:
        return "Content appears safe. No action needed."

    flagged = safety_result["flagged_categories"]
    recommendations = []

    if "hate" in flagged or "hate_threatening" in flagged:
        recommendations.append(
            "Content contains hate speech. Consider revising or filtering."
        )

    if "harassment" in flagged or "harassment_threatening" in flagged:
        recommendations.append(
            "Content contains harassment. Consider revising or filtering."
        )

    if (
        "self_harm" in flagged
        or "self_harm_instructions" in flagged
        or "self_harm_intent" in flagged
    ):
        recommendations.append(
            "Content contains self-harm references. Consider adding support resources."
        )

    if "sexual" in flagged or "sexual_minors" in flagged:
        recommendations.append(
            "Content contains sexual material. Consider age restrictions."
        )

    if "violence" in flagged or "violence_graphic" in flagged:
        recommendations.append(
            "Content contains violent material. Consider content warnings."
        )

    if not recommendations:
        recommendations.append(
            "Content flagged for unspecified reasons. Review manually."
        )

    return " | ".join(recommendations)
