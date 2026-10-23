import os
import requests
from typing import List, Dict, Optional


PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_script_safety(
    text: str, api_key: str = None, threshold: float = 0.7
) -> Dict[str, any]:
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY", "")

    attributes = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "INSULT",
        "PROFANITY",
        "THREAT",
        "SEXUALLY_EXPLICIT",
    ]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": ["en"],
    }

    response = requests.post(
        PERSPECTIVE_API_ENDPOINT,
        params={"key": api_key},
        json=payload,
    )
    response.raise_for_status()
    result = response.json()

    scores = {}
    flagged = []
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged.append(attr_name)

    is_safe = len(flagged) == 0

    return {
        "is_safe": is_safe,
        "scores": scores,
        "flagged_attributes": flagged,
        "threshold": threshold,
        "text_length": len(text),
    }


def check_batch_safety(
    texts: List[str], api_key: str = None, threshold: float = 0.7
) -> List[Dict[str, any]]:
    results = []
    for text in texts:
        result = check_script_safety(text, api_key=api_key, threshold=threshold)
        result["text"] = text
        results.append(result)
    return results


def get_safety_summary(safety_results: List[Dict[str, any]]) -> Dict[str, any]:
    total = len(safety_results)
    safe_count = sum(1 for r in safety_results if r.get("is_safe", False))
    unsafe_count = total - safe_count

    all_flagged = set()
    for r in safety_results:
        all_flagged.update(r.get("flagged_attributes", []))

    return {
        "total_scripts": total,
        "safe_count": safe_count,
        "unsafe_count": unsafe_count,
        "safety_rate": safe_count / total if total > 0 else 0.0,
        "flagged_categories": list(all_flagged),
    }
