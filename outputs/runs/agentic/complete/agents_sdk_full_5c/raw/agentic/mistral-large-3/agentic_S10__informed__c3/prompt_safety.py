import os
import requests
from typing import Dict, Any
from pydantic import BaseModel


class SafetyRequest(BaseModel):
    text: str
    threshold: float = 0.7


class SafetyResponse(BaseModel):
    is_safe: bool
    score: float
    categories: Dict[str, float]


def check_prompt_safety(text: str, threshold: float = 0.7) -> SafetyResponse:
    """
    Check prompts and generated text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"].keys()
    }
    
    max_score = max(scores.values())
    is_safe = max_score < threshold
    
    return SafetyResponse(
        is_safe=is_safe,
        score=max_score,
        categories=scores
    )