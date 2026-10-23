from typing import List
import requests
import os


def unsafe_copy_check(texts: List[str]) -> Dict[str, bool]:
    """Check localized copy for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = {}

    for text in texts:
        data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        response = requests.post(url, json=data)
        response.raise_for_status()
        toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        results[text] = toxicity_score < 0.7

    return results
