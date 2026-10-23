import os
import requests
from messaging_models import PubSubMessage, SafetyCheckResult


def check_message_safety(message: PubSubMessage) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    text_to_analyze = str(
        message.data
    )  # Assuming message.data contains the text to check

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    attribute_scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in result["attributeScores"]
    }

    # Define a simple safety threshold for demonstration
    is_safe = attribute_scores.get("TOXICITY", 0) < 0.5

    return SafetyCheckResult(
        message_id=message.id if message.id else "",
        is_safe=is_safe,
        scores=attribute_scores,
    )
