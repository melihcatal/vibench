import os
import requests
from typing import List

# Perspective API example (configurable via env vars)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

def check_safety(messages: List[str], attribute: str = "TOXICITY", threshold: float = 0.7) -> List[bool]:
    """Check a list of text messages for unsafe content using Perspective API.

    Returns a list of booleans indicating whether each message exceeds the threshold.
    """
    data = {
        "comment": {
            "text": "",
            "type": "PLAIN_TEXT"
        },
        "requestedAttributes": {
            attribute: {
                "scoreThreshold": threshold
            }
        },
        "language": "en"
    }
    results = []
    for msg in messages:
        data["comment"]["text"] = msg
        resp = requests.post(PERSPECTIVE_API_URL, json=data, headers={"x-api-key": PERSPECTIVE_API_KEY})
        resp.raise_for_status()
        scores = resp.json()["attributeScores"].get(attribute, {})
        summary = scores.get("summaryScore", {})
        results.append(summary.get("value", 0.0) >= threshold)
    return results

if __name__ == "__main__":
    # Demo: verify a few sample log lines
    samples = [
        "User login successful.",
        "User attempted SQL injection: ' OR 1=1 --'",
    ]
    safety = check_safety(samples, attribute="TOXICITY", threshold=0.5)
    for txt, safe in zip(samples, safety):
        print(f"{txt}  ->  {'SAFE' if safe else 'UNSAFE'}")
