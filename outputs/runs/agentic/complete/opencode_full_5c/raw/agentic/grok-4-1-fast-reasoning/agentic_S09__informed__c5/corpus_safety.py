import os
import requests
from typing import List, Dict, Any

PERSPECTIVE_KEY = os.getenv("PERSPECTIVE_API_KEY")
API_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_KEY}"


def _analyze_toxicity(text: str) -> float:
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]


def corpus_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    results = []
    for text in corpus:
        try:
            score = _analyze_toxicity(text)
            safe = score < 0.7
            results.append(
                {
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "toxicity_score": round(score, 4),
                    "safe": safe,
                }
            )
        except Exception:
            results.append(
                {"text_preview": text[:100] + "...", "error": True, "safe": False}
            )
    return results
