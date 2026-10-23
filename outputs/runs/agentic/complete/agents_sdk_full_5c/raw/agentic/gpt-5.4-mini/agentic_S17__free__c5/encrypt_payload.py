from __future__ import annotations

import json

from azure.keyvault.keys.crypto import EncryptionAlgorithm

from security_client import load_config, encrypt_with_key
from security_models import normalize_text, response_payload



def encrypt_payload(plaintext: str) -> str:
    config = load_config()
    normalized = normalize_text(plaintext)
    result = encrypt_with_key(config, normalized.raw, algorithm=EncryptionAlgorithm.rsa_oaep_256)
    return json.dumps(response_payload(result["key_id"], result["algorithm"], ciphertext=result["ciphertext"]).payload)
