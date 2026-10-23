import requests
import os
from typing import Dict, Any


# Moderation using Perspective API (Google)
def moderate_claims(text_claims: Dict[str, str]) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = {}
    for claim_name, claim_text in text_claims.items():
        if not claim_text or not isinstance(claim_text, str):
            results[claim_name] = {"moderated": False, "reason": "empty or invalid"}
            continue

        payload = {
            "comment": {"text": claim_text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        analysis = response.json()

        toxicity_score = analysis["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        results[claim_name] = {
            "moderated": toxicity_score > 0.7,
            "scores": {
                "toxicity": toxicity_score,
                "severe_toxicity": analysis["attributeScores"]["SEVERE_TOXICITY"][
                    "summaryScore"
                ]["value"],
                "identity_attack": analysis["attributeScores"]["IDENTITY_ATTACK"][
                    "summaryScore"
                ]["value"],
                "insult": analysis["attributeScores"]["INSULT"]["summaryScore"][
                    "value"
                ],
                "profanity": analysis["attributeScores"]["PROFANITY"]["summaryScore"][
                    "value"
                ],
            },
        }

    return results
