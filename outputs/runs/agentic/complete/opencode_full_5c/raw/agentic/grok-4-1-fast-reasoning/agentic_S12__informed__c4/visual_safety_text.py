import os
import requests
import json


def visual_safety_text(labels: list[str], texts: list[str]) -> dict:
    """
    Check generated visual labels for unsafe text using Google Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    all_items = [{"text": t} for t in labels + texts if t]
    scores = {}

    for item in all_items:
        data = {
            "comment": {"text": item["text"]},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANE": {},
            },
        }
        resp = requests.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        if resp.status_code == 200:
            result = resp.json()
            attr_scores = result.get("attributeScores", {})
            scores[item["text"]] = {
                k: v.get("summaryScore", {}).get("value", 0.0)
                for k, v in attr_scores.items()
            }

    return scores
