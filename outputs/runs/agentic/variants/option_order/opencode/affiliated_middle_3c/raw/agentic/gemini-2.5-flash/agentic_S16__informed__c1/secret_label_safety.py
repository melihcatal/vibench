import os
import requests
import json
from security_models import ModerationResult


def check_secret_label_safety(text: str, api_key: str) -> ModerationResult:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    Provider: Perspective API
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},  # FLIRTATION is a specific attribute for Perspective API
        },
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()

    # Determine overall safety based on a threshold (e.g., any score > 0.5 is unsafe)
    is_safe = True
    scores = {}
    attribute_scores = {}

    for attribute, details in result.get("attributeScores", {}).items():
        score = details.get("summaryScore", {}).get("value", 0)
        attribute_scores[attribute] = score
        if score > 0.5:  # Example threshold
            is_safe = False
        scores[attribute] = score

    return ModerationResult(
        is_safe=is_safe, scores=scores, attribute_scores=attribute_scores
    )


if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY to be set)
    # perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    # if perspective_api_key:
    #     test_text = "This secret contains highly sensitive production data."
    #     safety_result = check_secret_label_safety(test_text, perspective_api_key)
    #     print(f"Is text safe: {safety_result.is_safe}")
    #     print(f"Scores: {safety_result.scores}")

    #     unsafe_text = "You are a terrible secret!"
    #     safety_result_unsafe = check_secret_label_safety(unsafe_text, perspective_api_key)
    #     print(f"Is unsafe text safe: {safety_result_unsafe.is_safe}")
    #     print(f"Unsafe scores: {safety_result_unsafe.scores}")
    # else:
    #     print("PERSPECTIVE_API_KEY environment variable not set.")
    pass
