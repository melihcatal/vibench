import base64

from security_client import sign, verify, get_key_id
from security_models import SignatureRequest, VerificationResult, normalize_bytes


def sign_or_verify_key(message: str, signature: str = None, key_id: str = None):
    request = SignatureRequest(key_id=key_id or get_key_id(), message=message)
    message_bytes = normalize_bytes(request.message)
    if signature is None:
        response = sign(message_bytes, key_id=request.key_id)
        return VerificationResult(
            key_id=request.key_id,
            verified=True,
            metadata={
                "signature": base64.b64encode(response["Signature"]).decode("utf-8")
            },
        )
    verified = verify(message_bytes, base64.b64decode(signature), key_id=request.key_id)
    return VerificationResult(
        key_id=request.key_id,
        verified=bool(verified.get("SignatureValid", False)),
        metadata={"signing_algorithm": str(verified.get("SigningAlgorithm", ""))},
    )
