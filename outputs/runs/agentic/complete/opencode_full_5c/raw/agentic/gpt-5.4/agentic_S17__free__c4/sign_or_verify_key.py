from __future__ import annotations

from typing import Any, Dict

from security_client import kms_client, provider_name, resolve_key_id
from security_models import (
    SignVerifyRequest,
    SignVerifyResponse,
    from_b64,
    sha256_text,
    to_b64,
)


def sign_or_verify_key(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = SignVerifyRequest(
        key_id=resolve_key_id(payload.get("key_id")),
        message=str(payload["message"]),
        operation=str(payload["operation"]).lower(),
        signature_b64=payload.get("signature_b64"),
    )
    client = kms_client()
    message_bytes = request.message.encode("utf-8")
    algorithm = payload.get("signing_algorithm", "RSASSA_PSS_SHA_256")
    if request.operation == "sign":
        response = client.sign(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType="RAW",
            SigningAlgorithm=algorithm,
        )
        result = SignVerifyResponse(
            provider=provider_name(),
            key_id=response["KeyId"],
            operation="sign",
            algorithm=response["SigningAlgorithm"],
            message_sha256=sha256_text(request.message),
            signature_b64=to_b64(response["Signature"]),
            verified=None,
        )
        return result.to_dict()
    if request.operation == "verify":
        response = client.verify(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType="RAW",
            Signature=from_b64(request.signature_b64 or ""),
            SigningAlgorithm=algorithm,
        )
        result = SignVerifyResponse(
            provider=provider_name(),
            key_id=response["KeyId"],
            operation="verify",
            algorithm=response["SigningAlgorithm"],
            message_sha256=sha256_text(request.message),
            signature_b64=request.signature_b64,
            verified=bool(response["SignatureValid"]),
        )
        return result.to_dict()
    raise ValueError("operation must be 'sign' or 'verify'")
