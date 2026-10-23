import os
import json
import requests
from messaging_models import PubSubMessage


def is_message_safe(msg: PubSubMessage) -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    text = msg.data.get("text", json.dumps(msg.data, indent=2))[:10000]
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"API error: {response.text}")
    result = response.json()
    toxicity_score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.5
