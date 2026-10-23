import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def key_usage_summary(events: str) -> dict:
    config = load_security_config()
    response = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": f"Summarize key usage and crypto events for Azure Key Vault operations: {normalize_text(events)}"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "summary": normalize_text(data.get("output_text") or events)}


if __name__ == "__main__":
    print(json.dumps(key_usage_summary(normalize_text(os.getenv("EVENTS", "")))))
