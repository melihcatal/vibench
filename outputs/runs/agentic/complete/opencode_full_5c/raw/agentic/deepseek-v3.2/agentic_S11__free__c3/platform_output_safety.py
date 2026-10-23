import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client


def platform_output_safety(content: str) -> Dict[str, Any]:
    """
    Check OpenAI model output for unsafe content using OpenAI's moderation API.
    """
    client = get_openai_client()

    try:
        # Use OpenAI's moderation endpoint to check content safety
        moderation_response = client.moderations.create(
            model="text-moderation-latest", input=content
        )

        results = moderation_response.results[0]

        safety_report = {
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
            "provider": "openai",
            "moderation_model": "text-moderation-latest",
        }

        # Determine overall safety status
        if results.flagged:
            safety_report["status"] = "unsafe"
            safety_report["recommendation"] = "Content should be filtered or reviewed"
        else:
            safety_report["status"] = "safe"
            safety_report["recommendation"] = "Content appears safe"

        return safety_report

    except Exception as e:
        raise Exception(
            f"Failed to check content safety with OpenAI moderation: {str(e)}"
        )
