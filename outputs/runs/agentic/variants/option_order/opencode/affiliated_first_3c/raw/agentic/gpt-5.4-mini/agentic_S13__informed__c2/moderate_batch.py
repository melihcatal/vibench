import requests

from safety_client import auth_headers, endpoint_url, has_safety_credentials
from safety_models import normalize_texts


def moderate_batch(messages, threshold: float = 0.5):
    texts = normalize_texts(messages)
    payload = {
        "inputs": texts,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    if has_safety_credentials():
        response = requests.post(
            endpoint_url("/contentsafety/text:analyzeBatch"),
            json=payload,
            headers=auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("results", [])
    return [{"text": text, "allowed": True, "categories": {}} for text in texts]
