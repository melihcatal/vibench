import requests
from typing import List
from speech_models import ModerationResult

OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY = "openai_api_key"  # Expected in environment

def moderate_transcript(text: str) -> ModerationResult:
    """Moderate transcript text before publishing using OpenAI Moderation API."""
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"input": text}

    response = requests.post(OPENAI_MODERATION_API_URL, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()["results"][0]
    return ModerationResult(
        flagged=result["flagged"],
        categories=list(result["categories"].keys()),
        score=result["category_scores"]["harassment"],  # Example category
    )