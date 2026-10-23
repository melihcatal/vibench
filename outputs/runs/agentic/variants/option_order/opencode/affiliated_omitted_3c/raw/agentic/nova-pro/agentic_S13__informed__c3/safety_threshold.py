import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def safety_threshold(text, threshold=0.5):
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"][
        "value"
    ]
    return toxicity_score <= threshold
