import base64

from security_client import get_kms_client
from security_models import SignatureRequest, VerificationResult, normalize_text


def sign_or_verify_key(message: str, key_id: str, signature: str = ""):
    client = get_kms_client()
    req = SignatureRequest(
        message=normalize_text(message), key_id=normalize_text(key_id)
    )
    if signature:
        result = client.verify(
            KeyId=req.key_id,
            Message=req.message.encode("utf-8"),
            Signature=base64.b64decode(signature.encode("ascii")),
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return VerificationResult(
            valid=bool(result.get("SignatureValid", False)), key_id=req.key_id
        )
    signed = client.sign(
        KeyId=req.key_id,
        Message=req.message.encode("utf-8"),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "key_id": req.key_id,
        "signature": base64.b64encode(signed["Signature"]).decode("ascii"),
        "provider": "aws-kms",
    }
