from openai import OpenAI
from model_client import get_openai_config
from typing import Dict, Any


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    config = get_openai_config()
    client = OpenAI(**config)
    moderation = client.moderations.create(input=text)
    result = moderation.results[0]
    return {
        "safe": not result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
