import json
from typing import Any, Dict

import requests

from model_client import auth_params, default_headers, google_generate_url, model_name
from model_models import extract_text_from_response


def extract_json(text: str, schema_hint: str, model: str = "gemini-2.0-flash") -> Dict[str, Any]:
    prompt = f"Extract structured JSON matching this schema hint:\n{schema_hint}\n\nText:\n{text}\n\nReturn only valid JSON."
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    extracted = extract_text_from_response(data)
    return json.loads(extracted)
