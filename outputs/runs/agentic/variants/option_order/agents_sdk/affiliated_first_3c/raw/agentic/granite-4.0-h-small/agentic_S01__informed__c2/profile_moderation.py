import os
import requests
from pydantic import BaseModel, Field

# Load Perspective API key from env
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

class ModerationRequest(BaseModel):
    comment: dict = Field(default_factory=dict)  # JSON-serializable
    languages: list[str] = ['en']
    requested_attributes: dict = {
        'TOXICITY': 1.0,
        'SEVERE_TOXICITY': 1.0,
        'PROFANITY': 1.0,
        'IDENTITY_HATE': 1.0,
        'FLIRTATION': 1.0,
    }

class ModerationResponse(BaseModel):
    attribute_scores: dict
    languages: list[str]

def moderate_profile_text(text: str) -> ModerationResponse:
    """Moderate profile text before account activation using Perspective API.

    Returns the scores for toxicity and related attributes.
    """
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'PROFANITY': {},
            'IDENTITY_HATE': {},
            'FLIRTATION': {}
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': PERSPECTIVE_API_KEY
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return ModerationResponse(**response.json())
