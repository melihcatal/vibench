from __future__ import annotations

import json

from azure.keyvault.keys.crypto import EncryptionAlgorithm

from security_client import load_config, decrypt_with_key, b64decode
from security_models import normalize_b64, response_payload



def decrypt_payload(ciphertext_b64: str) -> str:
    config = load_config()
    normalized = normalize_b64(ciphertext_b64)
    result = decrypt_with_key(config, normalized.raw, algorithm=EncryptionAlgorithm.rsa_oaep_256)
    plaintext = result["plaintext"].decode("utf-8")
    return json.dumps(response_payload(result["key_id"], "RSA-OAEP-256", plaintext=plaintext).payload)
