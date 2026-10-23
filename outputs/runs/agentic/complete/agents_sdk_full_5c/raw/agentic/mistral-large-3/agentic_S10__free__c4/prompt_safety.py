import os
from typing import Dict, Any
from model_client import get_llm_client


def check_prompt_safety(text: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    client = get_llm_client()
    response = client.moderations.create(input=text)
    return {
        "flagged": response.results[0].flagged,
        "categories": response.results[0].categories.model_dump()
    }