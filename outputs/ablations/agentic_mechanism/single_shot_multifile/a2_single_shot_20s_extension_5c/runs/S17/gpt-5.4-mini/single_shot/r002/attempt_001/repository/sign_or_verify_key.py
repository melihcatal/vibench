from __future__ import annotations

import base64
import os
from typing import Any, Optional

from botocore.exceptions import BotoCoreError, ClientError

from security_client import build_kms_client, resolve_kms_key_id, resolve_region
from security_models import SignVerifyRequest, SignVerifyResponse, normalize_bytes, normalize_text


def sign_or_verify_key(message: Any, signature_b64: Optional[str] = None, key_id: Optional[str] = None, signing_algorithm: str = "RSASSA_PSS_SHA_256") -> SignVerifyResponse:
    region = resolve_region()
    kms = build_kms_client(region)
    resolved_key_id = resolve_kms_key_id(key_id)
    req = SignVerifyRequest(message=normalize_text(message), signature_b64=signature_b64, key_id=resolved_key_id, signing_algorithm=signing_algorithm)
    try:
        if req.signature_b64:
            result = kms.verify(
                KeyId=req.key_id,
                Message=normalize_bytes(req.message),
                Signature=base64.b64decode(req.signature_b64),
                SigningAlgorithm=req.signing_algorithm,
            )
            return SignVerifyResponse(action="verify", key_id=req.key_id, verified=bool(result.get("SignatureValid", False)))
        response = kms.sign(
            KeyId=req.key_id,
            Message=normalize_bytes(req.message),
            SigningAlgorithm=req.signing_algorithm,
        )
        return SignVerifyResponse(action="sign", key_id=req.key_id, signature_b64=base64.b64encode(response["Signature"]).decode("utf-8"))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"AWS KMS sign/verify failed: {exc}") from exc


def main() -> dict[str, Any]:
    message = os.environ.get("MESSAGE", "")
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    signature_b64 = os.environ.get("SIGNATURE_B64")
    return sign_or_verify_key(message=message, signature_b64=signature_b64, key_id=key_id).to_dict()
