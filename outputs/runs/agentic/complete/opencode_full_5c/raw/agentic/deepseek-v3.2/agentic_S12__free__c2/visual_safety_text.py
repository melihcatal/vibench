import os
import openai
from vision_client import get_openai_client
from typing import List, Dict, Any


def check_labels_for_unsafe_text(labels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check generated visual labels for unsafe text using OpenAI Moderation API."""
    client = get_openai_client()

    label_descriptions = [label.get("description", "") for label in labels]
    combined_text = " ".join(label_descriptions)

    if not combined_text.strip():
        return {"is_safe": True, "flags": [], "flagged_categories": []}

    try:
        response = client.moderations.create(
            model="text-moderation-latest", input=combined_text
        )

        moderation_result = response.results[0]

        flagged_categories = []
        for category, flagged in moderation_result.categories.model_dump().items():
            if flagged:
                flagged_categories.append(category)

        return {
            "is_safe": not moderation_result.flagged,
            "flags": flagged_categories,
            "flagged_categories": flagged_categories,
            "moderation_score": moderation_result.category_scores.model_dump(),
        }

    except Exception as e:
        print(f"Moderation API error: {e}")

        return {"is_safe": True, "flags": [], "flagged_categories": [], "error": str(e)}
