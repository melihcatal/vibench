from __future__ import annotations

import json
import os

from security_client import KMSSecurityClient
from security_models import PayloadRequest

PROVIDER = "AWS KMS"


def encrypt_payload(plaintext: str, key_id: str | None = None, context: dict[str, str] | None = None) -> str:
    client = KMSSecurityClient(region_name=os.environ.get("AWS_REGION"))
    request = PayloadRequest(plaintext=plaintext, key_id=key_id, context=context or {})
    response = client.encrypt(request)
    return json.dumps({"provider": PROVIDER, "key_id": response.key_id, "ciphertext_b64": response.ciphertext_b64, "metadata": response.metadata})
