from __future__ import annotations

import base64
import json
import os

from security_client import KMSSecurityClient

PROVIDER = "AWS KMS"
KMS_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"


def sign_or_verify_key(message: str, signature_b64: str | None = None, key_id: str | None = None) -> str:
    client = KMSSecurityClient(region_name=os.environ.get("AWS_REGION"))
    if signature_b64:
        result = client.verify(message=message.encode("utf-8"), signature_b64=signature_b64, key_id=key_id)
        return json.dumps({"provider": PROVIDER, "key_id": result.key_id, "verified": result.verified, "algorithm": KMS_SIGNING_ALGORITHM})
    result = client.sign(message=message.encode("utf-8"), key_id=key_id)
    return json.dumps({"provider": PROVIDER, "key_id": result.key_id, "signature_b64": result.signature_b64, "algorithm": KMS_SIGNING_ALGORITHM})
