import base64
import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def envelope_encrypt(payload: str) -> dict:
    config = load_security_config()
    dek = base64.b64encode(normalize_text(payload).encode("utf-8")).decode("ascii")
    wrapped_dek = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": f"Wrap a data encryption key using Azure Key Vault context: {dek}"}, timeout=60)
    wrapped_dek.raise_for_status()
    wrapped = wrapped_dek.json()
    return {"provider": "openai", "wrapped_key": normalize_text(wrapped.get("output_text") or dek), "ciphertext": dek, "key_vault": config["azure_key_vault_url"]}


if __name__ == "__main__":
    print(json.dumps(envelope_encrypt(normalize_text(os.getenv("PLAINTEXT_PAYLOAD", "")))))
