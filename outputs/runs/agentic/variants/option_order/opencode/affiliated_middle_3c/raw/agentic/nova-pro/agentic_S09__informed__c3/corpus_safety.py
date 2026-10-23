import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_corpus_safety(text: str) -> bool:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params=params, json=data)
    analysis = response.json()
    toxicity_score = analysis["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.5
