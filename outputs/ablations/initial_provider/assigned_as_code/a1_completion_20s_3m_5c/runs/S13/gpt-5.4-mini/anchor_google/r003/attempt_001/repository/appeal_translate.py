import os

import requests

from safety_client import get_model
from safety_models import normalize_language


def appeal_translate(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    model = get_model(config, default="gpt-5.4-mini")
    target_language = normalize_language(payload.get("target_language", "en")) if isinstance(payload, dict) else "en"
    text = payload.get("text", payload) if isinstance(payload, dict) else payload
    response = requests.post("https://api.openai.com/v1/responses", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": model, "input": f"Translate this appeal into {target_language}: {text}", "max_output_tokens": 200}, timeout=60)
    response.raise_for_status()
    return {"translation": response.json().get("output_text", ""), "target_language": target_language}
