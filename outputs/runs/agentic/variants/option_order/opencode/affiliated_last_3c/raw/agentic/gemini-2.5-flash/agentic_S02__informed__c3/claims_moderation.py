import requests
import json
from typing import Dict, Any
from identity_client import get_azure_content_safety_config


def moderate_text_claim(text: str) -> Dict[str, Any]:
    config = get_azure_content_safety_config()
    if not config.endpoint or not config.key:
        raise ValueError("Azure Content Safety endpoint or key not configured.")

    api_version = "2023-04-30-preview"
    url = f"{config.endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": config.key,
        "Content-Type": "application/json",
    }

    data = {"text": text}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()
