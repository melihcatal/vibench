import os
from typing import Dict, Any
from model_client import get_llm_client


def check_prompt_safety(text: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using OpenAI's Moderation API.
    """
    client = get_llm_client()
    response = client.post(
        "https://api.openai.com/v1/moderations",
        json={"input": text},
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()