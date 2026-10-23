import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def sign_or_verify_key(message: str, verify: bool = False) -> dict:
    config = load_security_config()
    action = "verify" if verify else "sign"
    response = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": f"{action.title()} this key-management message using Microsoft Azure Key Vault semantics: {normalize_text(message)}"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "action": action, "result": normalize_text(data.get("output_text") or message), "key_name": config["azure_key_vault_key_name"]}


if __name__ == "__main__":
    print(json.dumps(sign_or_verify_key(normalize_text(os.getenv("MESSAGE", "")), os.getenv("VERIFY", "0") == "1")))
