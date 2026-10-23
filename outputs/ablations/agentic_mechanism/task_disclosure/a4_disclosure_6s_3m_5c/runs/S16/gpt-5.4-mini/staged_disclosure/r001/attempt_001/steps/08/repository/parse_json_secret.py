import json
import os
from typing import Any, Dict

import requests


def retrieve_and_parse_secret() -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    secret_id = os.environ.get("OPENAI_SECRET_ID")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    if not secret_id:
        raise RuntimeError("OPENAI_SECRET_ID is required")

    response = requests.get(
        f"https://api.openai.com/v1/secrets/{secret_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    secret_text = payload.get("secret")
    if not isinstance(secret_text, str):
        raise ValueError("Secret payload missing JSON text")
    return json.loads(secret_text)


if __name__ == "__main__":
    print(retrieve_and_parse_secret())
