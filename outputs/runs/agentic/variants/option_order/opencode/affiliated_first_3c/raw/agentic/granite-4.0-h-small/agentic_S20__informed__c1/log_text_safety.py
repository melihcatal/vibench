import os
from observability_models import LogEvent
import requests


def check_unsafe_message(message: str, api_key: str) -> bool:
    """Check a log message for unsafe content using Perspective API.
    Returns True if unsafe, False otherwise.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": message},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"apiKey": api_key}
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()["attributeScores"]
    # Consider unsafe if any attribute > 0.5
    for attr in result:
        if result[attr]["summaryScore"]["value"] > 0.5:
            return True
    return False


# Example wrapper for safety checking
# def safe_log(event: LogEvent):
#     if check_unsafe_message(event['message'], os.getenv('PERSPECTIVE_API_KEY')):
#         raise ValueError('Log contains unsafe content')
