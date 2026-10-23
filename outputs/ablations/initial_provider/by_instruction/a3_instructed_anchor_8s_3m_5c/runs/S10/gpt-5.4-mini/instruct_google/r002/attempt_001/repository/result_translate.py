import requests

from model_client import auth_params, default_headers, google_generate_url, model_name
from model_models import extract_text_from_response


def result_translate(text: str, target_language: str, model: str = "gemini-2.0-flash") -> str:
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        timeout=60,
    )
    response.raise_for_status()
    return extract_text_from_response(response.json())
