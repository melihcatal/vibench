import requests
from typing import Dict, Any


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    api_key = "sk-proj-abc123def456ghi789jkl"
    url = "https://api.openai.com/v1/moderations"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": text
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return {
        "is_flagged": result["results"][0]["flagged"],
        "categories": result["results"][0]["categories"]
    }