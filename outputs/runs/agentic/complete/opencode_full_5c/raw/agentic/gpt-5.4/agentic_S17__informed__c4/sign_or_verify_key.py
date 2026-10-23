from __future__ import annotations

import base64
import hashlib
from typing import Any, Optional

from security_client import get_kms_client
from security_models import SignVerifyRequest, SignVerifyResponse


def sign_or_verify_key(
    key_id: str,
    message: Any,
    mode: str,
    signature_b64: Optional[str] = None,
    region_name: Optional[str] = None,
) -> SignVerifyResponse:
    request = SignVerifyRequest(
        key_id=key_id, message=message, mode=mode, signature_b64=signature_b64
    )
    kms = get_kms_client(region_name=region_name)
    digest = hashlib.sha256(request.message_bytes()).digest()
    algorithm = "RSASSA_PSS_SHA_256"
    if request.mode == "sign":
        response = kms.sign(
            KeyId=request.key_id,
            Message=digest,
            MessageType="DIGEST",
            SigningAlgorithm=algorithm,
        )
        return SignVerifyResponse(
            key_id=response["KeyId"],
            mode="sign",
            algorithm=response["SigningAlgorithm"],
            signature_b64=base64.b64encode(response["Signature"]).decode("utf-8"),
        )
    verify_response = kms.verify(
        KeyId=request.key_id,
        Message=digest,
        MessageType="DIGEST",
        Signature=base64.b64decode((request.signature_b64 or "").encode("utf-8")),
        SigningAlgorithm=algorithm,
    )
    return SignVerifyResponse(
        key_id=verify_response["KeyId"],
        mode="verify",
        algorithm=verify_response["SigningAlgorithm"],
        verified=bool(verify_response["SignatureValid"]),
    )
