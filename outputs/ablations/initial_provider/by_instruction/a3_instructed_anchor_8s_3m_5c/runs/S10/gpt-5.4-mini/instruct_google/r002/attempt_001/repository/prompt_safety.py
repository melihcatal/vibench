from typing import Dict

import requests

from model_client import auth_params, default_headers, google_generate_url, model_name


def prompt_safety(text: str, model: str = "gemini-2.0-flash") -> Dict[str, str]:
    prompt = f"Classify the following content for unsafe or harmful material. Return JSON with keys safe and reason.\n\n{text}"
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        timeout=60,
    )
    response.raise_for_status()
    return {"raw": response.text}
