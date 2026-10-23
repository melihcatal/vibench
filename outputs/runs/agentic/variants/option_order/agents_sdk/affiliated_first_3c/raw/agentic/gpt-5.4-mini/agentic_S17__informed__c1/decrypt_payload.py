from __future__ import annotations

import json
import os

from security_client import KMSSecurityClient
from security_models import normalize_text

PROVIDER = "AWS KMS"


def decrypt_payload(ciphertext_b64: str, context: dict[str, str] | None = None) -> str:
    client = KMSSecurityClient(region_name=os.environ.get("AWS_REGION"))
    result = client.decrypt(ciphertext_b64=ciphertext_b64, context=context or {})
    return json.dumps({"provider": PROVIDER, "key_id": result.key_id, "plaintext": normalize_text(result.plaintext), "context": result.context})
