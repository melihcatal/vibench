import os
import requests
from typing import List, Dict
from vision_models import ImageLabels

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
API_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"


def visual_safety_text(image_labels: ImageLabels) -> Dict[str, float]:
    labels = image_labels["labels"]
    results = {}
    for label in labels:
        payload = {"comment": {"text": label}, "requestedAttributes": {"TOXICITY": {}}}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            toxicity_score = response.json()["attributeScores"]["TOXICITY"][
                "summaryScore"
            ]["value"]
            results[label] = toxicity_score
        else:
            results[label] = 0.0
    return results
