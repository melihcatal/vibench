import base64
from typing import Optional

from security_client import SecurityClient
from security_models import VerificationRequest, normalize_payload


def sign_or_verify_key(
    message: str, signature: Optional[str] = None, key_id: Optional[str] = None
) -> dict:
    client = SecurityClient()
    req = VerificationRequest(
        key_id=key_id or client.kms_key_id(),
        message=normalize_payload(message),
        signature=signature,
    )
    if req.signature:
        sig = base64.b64decode(req.signature.encode("utf-8"))
        result = client.kms.verify(
            Message=req.message.encode("utf-8"),
            Signature=sig,
            KeyId=req.key_id,
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return {
            "key_id": req.key_id,
            "verified": bool(result.get("SignatureValid")),
            "algorithm": "aws-kms-verify",
        }
    signed = client.kms.sign(
        Message=req.message.encode("utf-8"),
        KeyId=req.key_id,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "key_id": req.key_id,
        "signature": base64.b64encode(signed["Signature"]).decode("utf-8"),
        "algorithm": "aws-kms-sign",
    }
