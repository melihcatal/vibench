import os
import requests
import json


def check_annotation_safety(
    text: str,
    perspective_api_key: str = os.environ.get("PERSPECTIVE_API_KEY", ""),
    api_base_url: str = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
) -> dict:
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{api_base_url}?key={perspective_api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()
