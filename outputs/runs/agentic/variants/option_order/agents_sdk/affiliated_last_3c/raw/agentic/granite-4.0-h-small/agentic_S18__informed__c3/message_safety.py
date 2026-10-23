import os
import requests

def check_safety(payload_text: str, api_key: str) -> bool:
    """Check whether the payload text contains unsafe content using Perspective API.",
    endpoint = "https://commentanalysis.googleapis.com/v1/comments:analyze"
    headers = {
        "content-type": "application/json",
        "x-api-key": api_key,
    }
    body = {
        "comment": {
            "text": payload_text
        },
        "languages": ["en"]
    }
    response = requests.post(endpoint, json=body, headers=headers)
    response.raise_for_status()
    result = response.json()
    # Example: if the toxicity score exceeds 0.8 consider unsafe
    toxicity = result.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value', 0.0)
    return toxicity < 0.8
