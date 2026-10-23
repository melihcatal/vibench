import os
from typing import Optional
import requests
from identity_models import ModerationResult


def moderate_claims_text(text: str, api_key: Optional[str] = None) -> ModerationResult:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    response = requests.post(
        url="https://api.openai.com/v1/moderations",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={"input": text},
    )
    response.raise_for_status()
    
    result = response.json()
    flags = []
    
    if result["results"][0]["flagged"]:
        categories = result["results"][0]["categories"]
        flags = [k for k, v in categories.items() if v]
    
    return ModerationResult(
        is_flagged=result["results"][0]["flagged"],
        flags=flags,
        sanitized_text=text if not flags else None,
    )