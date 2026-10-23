import base64
import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def decrypt_payload(ciphertext: str, key_name: str = ""):
    config = load_security_config()
    decoded = base64.b64decode(normalize_text(ciphertext)).decode("utf-8", errors="replace")
    prompt = f"Decrypt or interpret this managed-key protected payload for key {key_name or config['azure_key_vault_key_name']}: {decoded}"
    response = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": prompt}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "plaintext": normalize_text(data.get("output_text") or decoded), "key_name": key_name or config["azure_key_vault_key_name"]}


if __name__ == "__main__":
    ciphertext = normalize_text(os.getenv("CIPHERTEXT_PAYLOAD", ""))
    print(json.dumps(decrypt_payload(ciphertext)))
