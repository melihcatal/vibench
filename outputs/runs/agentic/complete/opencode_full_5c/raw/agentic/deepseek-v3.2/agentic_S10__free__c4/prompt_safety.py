import os
import json
from typing import Dict, Any
from openai import OpenAI
from model_client import get_client


def check_prompt_safety(prompt: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using OpenAI's moderation API.
    """
    client = get_client()

    try:
        response = client.moderations.create(
            input=prompt, model="text-moderation-latest"
        )

        result = response.results[0]

        safety_result = {
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
        }

        return safety_result
    except Exception as e:
        raise Exception(f"Failed to check prompt safety: {str(e)}")
