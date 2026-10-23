import os
import requests
from typing import List


class SafetyTextRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyTextResponse:
    def __init__(self, scores: dict):
        self.scores = scores


def check_visual_safety_text(request: SafetyTextRequest) -> SafetyTextResponse:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()

    scores = {
        "toxicity": result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    }
    return SafetyTextResponse(scores=scores)
