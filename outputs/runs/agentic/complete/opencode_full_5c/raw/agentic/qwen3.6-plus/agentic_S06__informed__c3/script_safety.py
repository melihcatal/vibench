from typing import Dict, List, Optional
import requests

PERSPECTIVE_API_KEY = ""
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(
    text: str,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> Dict:
    key = api_key or PERSPECTIVE_API_KEY
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]
    if languages is None:
        languages = ["en"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "spanAnnotations": False,
    }
    params = {"key": key}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, params=params)
    response.raise_for_status()
    result = response.json()
    scores = {}
    flagged = []
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged.append(attr_name)
    return {
        "safe": len(flagged) == 0,
        "flagged_attributes": flagged,
        "scores": scores,
        "threshold": threshold,
        "text_length": len(text),
    }


def check_safety_batch(
    texts: List[str],
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> List[Dict]:
    results = []
    for text in texts:
        result = check_safety(
            text=text,
            api_key=api_key,
            attributes=attributes,
            languages=languages,
            threshold=threshold,
        )
        results.append(result)
    return results
