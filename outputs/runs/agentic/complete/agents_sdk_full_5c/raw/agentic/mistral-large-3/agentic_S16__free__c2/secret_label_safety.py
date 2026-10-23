import os
import requests
from typing import Dict, List


def secret_label_safety(labels: Dict[str, str], api_key: str = None) -> List[dict]:
    """
    Check secret labels and notes for unsafe text using OpenAI Moderation API.
    
    Args:
        labels: Dictionary of secret labels (e.g., {"env": "prod", "team": "backend"}).
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
    
    Returns:
        List of moderation results for each label value.
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    moderation_results = []
    for key, value in labels.items():
        response = requests.post(
            "https://api.openai.com/v1/moderations",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"input": value}
        )
        result = response.json()
        moderation_results.append({
            "label": key,
            "value": value,
            "flagged": result["results"][0]["flagged"],
            "categories": result["results"][0]["categories"]
        })
    
    return moderation_results