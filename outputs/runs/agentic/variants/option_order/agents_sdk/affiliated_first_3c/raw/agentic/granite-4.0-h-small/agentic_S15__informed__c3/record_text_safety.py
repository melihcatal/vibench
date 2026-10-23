import os
import json
import requests
from pymongo import MongoClient

# -------------------------------------------------
# Provider setup (Azure AI Content Safety REST API)
# -------------------------------------------------
CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')


def check_text_safety(text, context=None):
    """
    Check user‑generated text for unsafe content using Azure AI Content Safety.

    Args:
        text (str): The text string to evaluate.
        context (dict, optional): Optional contextual metadata (e.g., user_id).

    Returns:
        dict: JSON payload containing safety verdicts (e.g., toxicity score). 
    """
    if not CONTENT_SAFETY_ENDPOINT or not CONTENT_SAFETY_KEY:
        raise RuntimeError('Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY')

    url = f"{CONTENT_SAFETY_ENDPOINT}/v1.0/checkContent"
    payload = {
        "input": {
            "kind": "text",
            "text": text
        }
    }
    if context:
        payload['context'] = context

    headers = {
        'Content-Type': 'application/json',
        'api-key': CONTENT_SAFETY_KEY
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Example usage with environment variables set
    result = check_text_safety(
        text="I think this plan is great!",
        context={'user_id': 'alice-001'}
    )
    print(json.dumps(result, indent=2))
