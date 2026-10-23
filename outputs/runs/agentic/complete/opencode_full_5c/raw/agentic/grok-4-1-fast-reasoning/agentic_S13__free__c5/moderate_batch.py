import os
from typing import List
from googleapiclient.discovery import build
from safety_models import ModerationResult


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    analyzer = build("commentanalyzer", "v1alpha1", developerKey=api_key)
    attributes = [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
        "SEXUALLY_EXPLICIT",
    ]
    results = []
    for text in texts:
        request = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
        }
        response = analyzer.comments().analyze(body=request).execute()
        scores = response["attributeScores"]
        categories = {k.lower(): scores[k]["summaryScore"]["value"] for k in attributes}
        flagged = any(score > 0.5 for score in categories.values())
        results.append(
            {
                "input_text": text,
                "flagged": flagged,
                "categories": categories,
                "rationale": None,
            }
        )
    return results
