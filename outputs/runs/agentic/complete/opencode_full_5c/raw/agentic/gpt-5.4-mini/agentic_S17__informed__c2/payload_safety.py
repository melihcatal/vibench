import json
import os

import requests

from security_models import OperationResult, normalize_text


def payload_safety(payload):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": api_key},
        json={
            "comment": {"text": normalize_text(payload)},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    data = response.json()
    score = (
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return OperationResult(ok=True, data={"unsafe": score >= 0.5, "score": score})


def main():
    print(json.dumps({"status": "ready"}))


if __name__ == "__main__":
    main()
