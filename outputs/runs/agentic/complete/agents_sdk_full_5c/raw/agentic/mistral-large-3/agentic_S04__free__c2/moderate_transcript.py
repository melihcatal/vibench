import requests
from typing import List, Dict, Optional
from pydantic import BaseModel

class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    flagged: bool
    categories: Optional[Dict[str, bool]]
    error: Optional[str]

def moderate_transcript(text: str) -> ModerationResponse:
    """
    Moderates transcript text using OpenAI Moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"input": text}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return ModerationResponse(
            flagged=result["results"][0]["flagged"],
            categories=result["results"][0]["categories"],
            error=None
        )
    except Exception as e:
        return ModerationResponse(
            flagged=False,
            categories=None,
            error=str(e)
        )