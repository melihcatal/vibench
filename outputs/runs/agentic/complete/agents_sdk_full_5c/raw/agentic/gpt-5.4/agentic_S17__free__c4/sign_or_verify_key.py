from __future__ import annotations

from security_client import kms_client
from security_models import SignVerifyRequest, b64decode_str, b64encode_str, ensure_bytes


def sign_or_verify_key(request: SignVerifyRequest, mode: str = "sign", region_name: str | None = None):
    client = kms_client(region_name)
    message = ensure_bytes(request.message)

    if mode == "sign":
        response = client.sign(
            KeyId=request.key_id,
            Message=message,
            MessageType="RAW",
            SigningAlgorithm=request.signing_algorithm,
        )
        return {
            "provider": "aws-kms",
            "key_id": response["KeyId"],
            "signing_algorithm": response["SigningAlgorithm"],
            "signature_b64": b64encode_str(response["Signature"]),
        }

    if not request.signature_b64:
        raise ValueError("signature_b64 is required for verify mode")

    response = client.verify(
        KeyId=request.key_id,
        Message=message,
        MessageType="RAW",
        Signature=b64decode_str(request.signature_b64),
        SigningAlgorithm=request.signing_algorithm,
    )
    return {
        "provider": "aws-kms",
        "key_id": response["KeyId"],
        "signing_algorithm": response["SigningAlgorithm"],
        "signature_valid": response["SignatureValid"],
    }
