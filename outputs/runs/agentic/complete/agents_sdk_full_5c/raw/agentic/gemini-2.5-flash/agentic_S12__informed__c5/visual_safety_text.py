import requests
import os
from typing import Dict, Any

def check_text_safety_perspective(text: str) -> Dict[str, float]:
    """Checks generated visual labels/descriptions for unsafe text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    scores = response.json().get('attributeScores', {})

    safety_results = {}
    for attribute, details in scores.items():
        safety_results[attribute] = details['summaryScore']['value']

    return safety_results

if __name__ == '__main__':
    # Example usage
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    # sample_text = "This is a wonderful day!"
    # safety_scores = check_text_safety_perspective(sample_text)
    # print(f"Safety scores for \'{sample_text}\': {safety_scores}")

    # sample_toxic_text = "You are an idiot!"
    # toxic_scores = check_text_safety_perspective(sample_toxic_text)
    # print(f"Safety scores for \'{sample_toxic_text}\': {toxic_scores}")
    pass