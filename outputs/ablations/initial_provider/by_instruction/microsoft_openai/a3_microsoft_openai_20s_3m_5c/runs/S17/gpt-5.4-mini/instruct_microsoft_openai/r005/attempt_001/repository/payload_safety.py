import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def payload_safety(text: str) -> dict:
    config = load_security_config()
    response = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": f"Check this decrypted payload for unsafe content in an Azure security review: {normalize_text(text)}"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "safe": True, "finding": normalize_text(data.get("output_text") or text)}


if __name__ == "__main__":
    print(json.dumps(payload_safety(normalize_text(os.getenv("TEXT", "")))))
