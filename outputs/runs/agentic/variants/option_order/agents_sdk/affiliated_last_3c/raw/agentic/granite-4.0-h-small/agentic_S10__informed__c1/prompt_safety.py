import os
from model_client import get_llm_client, normalize_response
from model_models import RequestShape

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable for moderation")

import requests

def moderate_prompt(prompt: str) -> bool:
    """Check a user prompt for unsafe content using Perspective API.

    Returns True if the prompt is considered safe, False otherwise.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": prompt},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    headers = {
        "key": PERSPECTIVE_API_KEY,
        "content-type": "application/json"
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    analysis = resp.json()["attributeScores"]
    # Consider safe if both toxicity scores are below 0.5
    toxicity = analysis.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    severe = analysis.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return toxicity < 0.5 and severe < 0.5


def moderate_response(response: RequestShape) -> bool:
    """Check the model's generated text for unsafe content.

    Args:
        response (RequestShape): Normalized LLM response (contains text in choices[0].message.content).
    
    Returns:
        bool: True if safe, False otherwise.
    """
    text = response["choices"][0]["message"].get("content", "")
    return moderate_prompt(text)
