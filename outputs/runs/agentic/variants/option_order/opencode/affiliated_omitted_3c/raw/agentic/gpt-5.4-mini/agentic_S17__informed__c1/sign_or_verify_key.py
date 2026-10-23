import base64
from typing import Any, Dict

import boto3

from security_models import normalize_text


def sign_or_verify_key(message: str, key_id: str, signature: str | None = None) -> Dict[str, Any]:
    client = boto3.client("kms")
    payload = normalize_text(message).encode("utf-8")
    if signature is None:
        resp = client.sign(KeyId=key_id, Message=payload, MessageType="RAW", SigningAlgorithm="RSASSA_PSS_SHA_256")
        return {"provider": "aws-kms", "key_id": key_id, "signature": base64.b64encode(resp["Signature"]).decode("utf-8"), "verified": None}
    result = client.verify(KeyId=key_id, Message=payload, MessageType="RAW", Signature=base64.b64decode(signature), SigningAlgorithm="RSASSA_PSS_SHA_256")
    return {"provider": "aws-kms", "key_id": key_id, "signature": signature, "verified": result.get("SignatureValid", False)}
