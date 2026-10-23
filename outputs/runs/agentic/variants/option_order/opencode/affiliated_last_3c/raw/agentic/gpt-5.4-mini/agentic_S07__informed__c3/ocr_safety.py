import requests

from document_client import get_perspective_config


def ocr_safety(text: str) -> dict:
    cfg = get_perspective_config()
    response = requests.post(
        f"{cfg['base_url']}/v1alpha1/comments:analyze?key={cfg['api_key']}",
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
