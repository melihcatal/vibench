import os
import requests
import json
from database_models import Document, SafetyResult
from typing import List, Dict, Any

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety(
    documents: List[Document], fields_to_check: List[str]
) -> List[SafetyResult]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    safety_results = []
    for doc in documents:
        full_text_to_analyze = " ".join(
            [str(doc.data.get(field, "")) for field in fields_to_check]
        )
        if not full_text_to_analyze.strip():
            safety_results.append(SafetyResult(id=doc.id, is_safe=True, scores={}))
            continue

        headers = {"Content-Type": "application/json"}
        params = {"key": api_key}
        body = {
            "comment": {"text": full_text_to_analyze},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
                "FLIRTATION": {},
            },
            "languages": ["en"],
        }

        response = requests.post(
            PERSPECTIVE_API_BASE_URL,
            headers=headers,
            params=params,
            data=json.dumps(body),
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        result = response.json()
        attribute_scores = {
            attr: result["attributeScores"][attr]["summaryScore"]["value"]
            for attr in result.get("attributeScores", {})
        }

        # A simple heuristic for safety: if any score is above a threshold (e.g., 0.5)
        is_safe = (
            all(score < 0.5 for score in attribute_scores.values())
            if attribute_scores
            else True
        )

        safety_results.append(
            SafetyResult(id=doc.id, is_safe=is_safe, scores=attribute_scores)
        )

    return safety_results
