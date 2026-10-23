import requests

from model_client import auth_params, default_headers, google_generate_url, model_name
from model_models import extract_text_from_response


def spoken_brief(text: str, model: str = "gemini-2.0-flash") -> str:
    prompt = f"Convert the following into a short spoken brief suitable for audio narration:\n\n{text}"
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        timeout=60,
    )
    response.raise_for_status()
    return extract_text_from_response(response.json())
