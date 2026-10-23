import requests
import os


def check_content_safety(text, api_key=None):
    if not api_key:
        api_key = os.getenv("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable not set or provided."
        )

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()
    toxicity_score = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
    )

    return {"toxicity_score": toxicity_score}
