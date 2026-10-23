from typing import Any, Dict

import requests

from model_client import auth_params, default_headers, google_generate_url, model_name
from model_models import extract_text_from_response


def answer_with_context(context: str, question: str, model: str = "gemini-2.0-flash") -> str:
    prompt = f"Use the context to answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = requests.post(
        google_generate_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        timeout=60,
    )
    response.raise_for_status()
    return extract_text_from_response(response.json())
