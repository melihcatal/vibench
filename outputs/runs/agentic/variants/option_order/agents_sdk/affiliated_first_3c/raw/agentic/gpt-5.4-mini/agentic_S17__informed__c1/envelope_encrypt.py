from __future__ import annotations

import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import KMSSecurityClient
from security_models import EnvelopeEncryptionResult

PROVIDER = "AWS KMS"


def envelope_encrypt(plaintext: str, key_id: str | None = None, context: dict[str, str] | None = None) -> str:
    client = KMSSecurityClient(region_name=os.environ.get("AWS_REGION"))
    material = client.generate_data_key(key_id=key_id, context=context or {})
    data_key = base64.b64decode(material["plaintext_data_key_b64"])
    aesgcm = AESGCM(data_key)
    nonce = os.urandom(12)
    aad = json.dumps(context or {}, sort_keys=True).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad)
    result = EnvelopeEncryptionResult(
        encrypted_data_key_b64=material["encrypted_data_key_b64"],
        ciphertext_b64=base64.b64encode(nonce + ciphertext).decode("ascii"),
        key_id=material.get("key_id"),
        metadata={"provider": PROVIDER, **material.get("metadata", {})},
    )
    return json.dumps(result.__dict__)
