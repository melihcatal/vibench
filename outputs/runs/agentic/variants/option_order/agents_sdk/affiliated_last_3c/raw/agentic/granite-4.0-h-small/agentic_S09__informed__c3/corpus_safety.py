import os
import requests

def check_corpus_safety(text: str, api_key: str) -> bool:
    """Check whether a corpus text meets content safety guidelines using Perspective API.

    Args:
        text (str): The text to evaluate.
        api_key (str): Perspective API key.

    Returns:
        bool: True if the text passes the toxicity threshold, False otherwise.
    """
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "key": api_key
    }
    resp = requests.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    # Threshold 0.5 as an example
    return score < 0.5
