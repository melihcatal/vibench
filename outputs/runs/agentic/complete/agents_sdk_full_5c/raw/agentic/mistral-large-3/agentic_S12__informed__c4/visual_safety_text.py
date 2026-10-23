import os
from typing import List, Dict
import requests
from vision_models import LabelDetectionResponse


def check_visual_labels_for_unsafe_text(labels: LabelDetectionResponse) -> Dict[str, bool]:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = {}
    for label in labels.labels:
        response = requests.post(
            url,
            json={
                "comment": {"text": label},
                "requestedAttributes": {"TOXICITY": {}}
            }
        )
        response.raise_for_status()
        toxicity_score = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
        results[label] = toxicity_score < 0.5

    return results