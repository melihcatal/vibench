import requests
import os
from security_models import parse_decrypted

def check_payload_safety(ciphertext: bytes, key_id: str, threshold: float = 0.5) -> dict:
    from decrypt_payload import get_decrypted_text
    text = get_decrypted_text(ciphertext, key_id)
    return check_text_safety(text, threshold)

def check_text_safety(text: str, threshold: float = 0.5) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        }
    }
    params = {"key": api_key}
    response = requests.post(url, json=data, params=params)
    result = response.json()
    # Apply threshold
    for attr, scores in result.get('attributeScores', {}).items():
        result['attributeScores'][attr]['above_threshold'] = scores['summaryScore']['value'] > threshold
    return result