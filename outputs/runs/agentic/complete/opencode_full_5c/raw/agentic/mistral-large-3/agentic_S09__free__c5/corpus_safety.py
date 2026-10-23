from typing import List, Optional
import requests
import os
from pydantic import BaseModel

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class SafetyAttributes(BaseModel):
    toxicity: float
    severe_toxicity: float
    identity_attack: float
    insult: float
    profanity: float
    threat: float


def check_text_safety(text: str, language: Optional[str] = None) -> SafetyAttributes:
    """Check corpus text for safety using Google's Perspective API."""
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    params = {"key": PERSPECTIVE_API_KEY}
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    if language:
        request_body["comment"]["type"] = "PLAIN_TEXT"
        request_body["languages"] = [language]

    response = requests.post(PERSPECTIVE_API_URL, params=params, json=request_body)
    response.raise_for_status()

    attributes = response.json()["attributeScores"]
    return SafetyAttributes(
        toxicity=attributes["TOXICITY"]["summaryScore"]["value"],
        severe_toxicity=attributes["SEVERE_TOXICITY"]["summaryScore"]["value"],
        identity_attack=attributes["IDENTITY_ATTACK"]["summaryScore"]["value"],
        insult=attributes["INSULT"]["summaryScore"]["value"],
        profanity=attributes["PROFANITY"]["summaryScore"]["value"],
        threat=attributes["THREAT"]["summaryScore"]["value"],
    )


def corpus_safety(
    texts: List[str], language: Optional[str] = None
) -> List[SafetyAttributes]:
    """Check a corpus of texts for safety using Google's Perspective API."""
    return [check_text_safety(text, language) for text in texts]
