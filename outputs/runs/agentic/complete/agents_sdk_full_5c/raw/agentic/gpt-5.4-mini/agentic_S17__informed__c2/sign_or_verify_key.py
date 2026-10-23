from __future__ import annotations

import base64
from typing import Any, Dict

from google.cloud import kms_v1

from security_client import get_google_kms_client
from security_models import CryptoRequest, CryptoResponse, normalize_text_payload


def sign_or_verify_key(request: CryptoRequest) -> CryptoResponse:
    client: kms_v1.KeyManagementServiceClient = get_google_kms_client()
    message = normalize_text_payload(request.signing_message or request.plaintext).encode("utf-8")
    digest = kms_v1.Digest(sha256=__import__("hashlib").sha256(message).digest())
    if request.ciphertext:
        signature = base64.b64decode(normalize_text_payload(request.ciphertext))
        verified = False
        try:
            verified = client.asymmetric_verify(request={"name": request.key_name, "digest": digest, "signature": signature}).verified
        except Exception:
            verified = False
        payload = "verified" if verified else "not_verified"
        op = "verify"
    else:
        response = client.asymmetric_sign(request={"name": request.key_name, "digest": digest})
        payload = base64.b64encode(response.signature).decode("ascii")
        op = "sign"
    metadata: Dict[str, Any] = {"provider": "google-cloud-kms"}
    return CryptoResponse(key_name=request.key_name, operation=op, payload=payload, metadata=metadata)


if __name__ == "__main__":
    pass
