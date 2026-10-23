import os
import requests
from model_client import get_openai_api_key

def check_prompt_safety(text: str, api_key: str = os.getenv("PERSPECTIVE_API_KEY")) -> bool:
    """Check whether the supplied text is likely unsafe using Google Perspective API.

    Returns True if safe (score < 0.5 for SEVERE_TOXICITY), False otherwise.
    """
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"SEVERE_TOXICITY": {}}
    }
    headers = {"key": api_key}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    score = resp.json()["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"]
    return score < 0.5

if __name__ == "__main__":
    sample = "This is a harmless comment."
    print(f"{sample} -> safe: {check_prompt_safety(sample)}")
