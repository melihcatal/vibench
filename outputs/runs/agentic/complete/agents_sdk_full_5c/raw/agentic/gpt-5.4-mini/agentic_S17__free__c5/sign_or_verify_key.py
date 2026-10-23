from __future__ import annotations

import hashlib
import json

from azure.keyvault.keys.crypto import SignatureAlgorithm

from security_client import load_config, sign_with_key, verify_with_key
from security_models import normalize_text, response_payload



def sign_or_verify_key(message: str, signature_b64: str | None = None) -> str:
    config = load_config()
    normalized = normalize_text(message)
    digest = hashlib.sha256(normalized.raw).digest()
    if signature_b64:
        import base64
        signature = base64.b64decode(signature_b64.encode("utf-8"))
        result = verify_with_key(config, digest, signature, algorithm=SignatureAlgorithm.rs256)
        return json.dumps(response_payload(result["key_id"], result["algorithm"], is_valid=result["is_valid"]).payload)
    result = sign_with_key(config, digest, algorithm=SignatureAlgorithm.rs256)
    return json.dumps(response_payload(result["key_id"], result["algorithm"], signature=result["signature"]).payload)
