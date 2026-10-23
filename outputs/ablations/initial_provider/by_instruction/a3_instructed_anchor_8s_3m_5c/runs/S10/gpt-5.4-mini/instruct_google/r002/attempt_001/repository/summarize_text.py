import json
from typing import Any, Dict

import requests

from model_client import auth_params, default_headers, google_generate_url, model_name
from model_models import extract_text_from_response


def summarize_text(text: str, model: str = "gemini-2.0-flash") -> str:
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Summarize the following text concisely:\n\n{text}"}],
            }
        ]
    }
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return extract_text_from_response(data)
