from typing import Any, Dict, List
import requests
import os


def check_text_safety(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    api_key = os.getenv("GOOGLE_PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = []
    for record in records:
        document = record.get("document", {})
        text = document.get("content", "")

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
            },
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        analysis = response.json()

        results.append(
            {
                "id": record["id"],
                "partition_key": record["partition_key"],
                "safety_scores": analysis.get("attributeScores", {}),
            }
        )

    return results
