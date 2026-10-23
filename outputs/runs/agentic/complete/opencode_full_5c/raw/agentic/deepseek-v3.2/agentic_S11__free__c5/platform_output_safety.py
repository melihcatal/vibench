import os
from typing import Dict, Any, List
from openai import OpenAI
from model_client import get_openai_client


def check_platform_output_safety(content: str) -> Dict[str, Any]:
    """Check platform model output for unsafe content using OpenAI's moderation API."""
    client = get_openai_client()

    # Use OpenAI's moderation endpoint to check for unsafe content
    response = client.moderations.create(model="text-moderation-latest", input=content)

    result = response.results[0]

    # Extract safety scores and flags
    safety_check = {
        "flagged": result.flagged,
        "categories": {
            "hate": result.categories.hate,
            "hate_threatening": result.categories.hate_threatening,
            "self_harm": result.categories.self_harm,
            "sexual": result.categories.sexual,
            "sexual_minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence_graphic": result.categories.violence_graphic,
        },
        "category_scores": {
            "hate": result.category_scores.hate,
            "hate_threatening": result.category_scores.hate_threatening,
            "self_harm": result.category_scores.self_harm,
            "sexual": result.category_scores.sexual,
            "sexual_minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence_graphic": result.category_scores.violence_graphic,
        },
        "moderation_id": response.id,
        "model": response.model,
    }

    # Determine overall safety status
    if result.flagged:
        safety_check["safety_status"] = "unsafe"
        safety_check["recommendation"] = "Content should be filtered or reviewed"
    else:
        safety_check["safety_status"] = "safe"
        safety_check["recommendation"] = "Content appears safe"

    return safety_check


def check_multiple_contents(contents: List[str]) -> List[Dict[str, Any]]:
    """Check multiple content strings for safety."""
    client = get_openai_client()

    # Batch moderation check
    response = client.moderations.create(model="text-moderation-latest", input=contents)

    results = []
    for i, result in enumerate(response.results):
        safety_check = {
            "content_preview": contents[i][:100] + "..."
            if len(contents[i]) > 100
            else contents[i],
            "flagged": result.flagged,
            "categories": {
                "hate": result.categories.hate,
                "hate_threatening": result.categories.hate_threatening,
                "self_harm": result.categories.self_harm,
                "sexual": result.categories.sexual,
                "sexual_minors": result.categories.sexual_minors,
                "violence": result.categories.violence,
                "violence_graphic": result.categories.violence_graphic,
            },
            "moderation_id": response.id,
            "model": response.model,
        }
        results.append(safety_check)

    return results


def get_safety_thresholds() -> Dict[str, float]:
    """Get recommended safety thresholds for different categories."""
    # OpenAI's default thresholds for moderation
    return {
        "hate": 0.5,
        "hate_threatening": 0.5,
        "self_harm": 0.5,
        "sexual": 0.5,
        "sexual_minors": 0.5,
        "violence": 0.5,
        "violence_graphic": 0.5,
    }


def is_content_safe(content: str, custom_thresholds: Dict[str, float] = None) -> bool:
    """Check if content is safe based on thresholds."""
    safety_check = check_platform_output_safety(content)

    if safety_check["flagged"]:
        return False

    thresholds = custom_thresholds or get_safety_thresholds()

    # Check each category against thresholds
    for category, score in safety_check["category_scores"].items():
        threshold = thresholds.get(category, 0.5)
        if score > threshold:
            return False

    return True


if __name__ == "__main__":
    # Example usage
    test_content = "This is a friendly message about technology and innovation."
    safety_result = check_platform_output_safety(test_content)

    print("Safety check result:")
    print(f"Flagged: {safety_result['flagged']}")
    print(f"Safety status: {safety_result['safety_status']}")
    print(f"Recommendation: {safety_result['recommendation']}")

    # Check multiple contents
    contents = [
        "Hello world!",
        "This is a test of the safety system.",
        "I hate everyone and want to cause harm.",  # This should be flagged
    ]

    batch_results = check_multiple_contents(contents)
    print("\nBatch safety check:")
    for i, result in enumerate(batch_results):
        print(f"Content {i + 1}: Flagged={result['flagged']}")
