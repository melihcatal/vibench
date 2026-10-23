import os
import requests


def check_visual_labels_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    result = response.json()
    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"toxicity_score": toxicity_score}
