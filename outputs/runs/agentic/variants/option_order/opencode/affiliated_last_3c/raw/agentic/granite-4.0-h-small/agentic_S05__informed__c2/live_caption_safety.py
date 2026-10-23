# [LATER-STEP] live_caption_safety.py
# Check live transcript text for unsafe content using Perspective API
import os
import requests

# Provider configuration
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

# Endpoint for analyzeComment
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def check_safety(text):
    payload = {
        "comment": {
            "text": text,
        },
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY, "content-type": "application/json"}
    response = requests.post(PERSPECTIVE_URL, json=payload, headers=headers)
    result = response.json()
    # Extract toxicity scores (example)
    toxicity = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return toxicity


if __name__ == "__main__":
    # Placeholder for live caption text
    score = check_safety("This is a test comment")
    print(f"Toxicity score: {score}")
