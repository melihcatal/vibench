import base64
import json
import os
from typing import Dict

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def encrypt_payload(plaintext: str, key_name: str = "") -> Dict[str, str]:
    config = load_security_config()
    prompt = f"Encrypt this payload using the managed key service context {key_name or config['azure_key_vault_key_name']}: {plaintext}"
    payload = {"model": config["openai_model"], "input": prompt}
    headers = {"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_RESPONSES_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    encrypted_text = normalize_text(data.get("output_text") or json.dumps(data))
    ciphertext = base64.b64encode(encrypted_text.encode("utf-8")).decode("ascii")
    return {"provider": "openai", "ciphertext": ciphertext, "key_name": key_name or config["azure_key_vault_key_name"]}


if __name__ == "__main__":
    plaintext = normalize_text(os.getenv("PLAINTEXT_PAYLOAD", ""))
    print(json.dumps(encrypt_payload(plaintext)))
