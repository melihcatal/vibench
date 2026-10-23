import os
import requests
from typing import Dict, Any


def check_record_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    user_texts = [record.get("body", ""), record.get("title", "")]
    text = " ".join(t for t in user_texts if t)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=data
    )
    response.raise_for_status()
    result = response.json()["results"][0]

    return {
        "flagged": result["flagged"],
        "categories": result["categories"],
        "category_scores": result["category_scores"],
    }
