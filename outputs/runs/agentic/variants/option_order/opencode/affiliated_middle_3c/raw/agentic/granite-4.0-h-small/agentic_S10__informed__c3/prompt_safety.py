import os
import requests

# Identify provider in code
PROVIDER = "Perspective API"

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def is_prompt_safe(prompt: str, severity_threshold: float = 0.5) -> bool:
    payload = {
        "comment": {"text": prompt},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY, "content-type": "application/json"}
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    attrs = response.json().get("attributeScores", {})
    toxicity = attrs.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    severe_toxicity = (
        attrs.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    )
    # Consider unsafe if severe toxicity or high toxicity
    return severe_toxicity < 0.5 and toxicity < severity_threshold
