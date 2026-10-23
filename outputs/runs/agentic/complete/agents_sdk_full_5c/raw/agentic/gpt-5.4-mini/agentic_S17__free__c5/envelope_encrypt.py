from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from typing import Dict

from azure.keyvault.keys.crypto import EncryptionAlgorithm
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import b64encode, load_config, encrypt_with_key, secret_client
from security_models import normalize_text, response_payload


@dataclass
class EnvelopeResult:
    encrypted_key: str
    nonce: str
    ciphertext: str
    key_id: str
    algorithm: str



def envelope_encrypt(plaintext: str) -> str:
    config = load_config()
    normalized = normalize_text(plaintext)
    dek = os.urandom(32)
    nonce = os.urandom(12)
    aesgcm = AESGCM(dek)
    ciphertext = aesgcm.encrypt(nonce, normalized.raw, None)
    wrapped = encrypt_with_key(config, dek, algorithm=EncryptionAlgorithm.rsa_oaep_256)
    result = EnvelopeResult(
        encrypted_key=wrapped["ciphertext"],
        nonce=b64encode(nonce),
        ciphertext=b64encode(ciphertext),
        key_id=wrapped["key_id"],
        algorithm=wrapped["algorithm"],
    )
    return json.dumps(asdict(result))
