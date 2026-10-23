import os
from typing import Any, Dict

from safety_models import normalize_messages, normalize_text

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key() -> str:
    key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    return key


def base_payload(text: str) -> Dict[str, Any]:
    return {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {},
        },
    }


def batch_payload(messages: Any) -> Dict[str, Any]:
    return {"messages": normalize_messages(messages)}
