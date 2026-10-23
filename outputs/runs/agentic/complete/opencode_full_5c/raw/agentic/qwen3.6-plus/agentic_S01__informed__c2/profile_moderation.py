import os
import requests
from typing import Dict, List, Optional, Any

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def moderate_profile_text(
    text: str,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
    languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    attrs = attributes or DEFAULT_ATTRIBUTES
    langs = languages or ["en"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attrs},
        "languages": langs,
        "doNotStore": True,
    }
    params = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(
        PERSPECTIVE_API_URL,
        json=payload,
        params=params,
        timeout=15,
    )
    resp.raise_for_status()
    result = resp.json()
    return _evaluate_moderation(result, threshold)


def _evaluate_moderation(
    api_response: Dict[str, Any],
    threshold: float,
) -> Dict[str, Any]:
    attribute_scores = api_response.get("attributeScores", {})
    flags = []
    scores = {}
    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flags.append(attr_name)
    return {
        "passed": len(flags) == 0,
        "flags": flags,
        "scores": scores,
        "threshold": threshold,
        "raw": api_response,
    }


def moderate_profile_batch(
    texts: List[str],
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
    languages: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    results = []
    for text in texts:
        result = moderate_profile_text(text, attributes, threshold, languages)
        results.append(result)
    return results
