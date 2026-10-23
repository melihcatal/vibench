from typing import Union, Literal, Optional
import os
from security_client import SecurityClient
from security_models import SigningResult, VerificationResult, normalize_payload


def sign_or_verify_key(
    key_id: str,
    data: Union[str, bytes, dict],
    mode: Literal["sign", "verify"],
    signature: Optional[bytes] = None,
) -> Union[SigningResult, VerificationResult]:
    """Signs or verifies data using Google Cloud KMS asymmetric keys."""
    client = SecurityClient()
    normalized_data = normalize_payload(data)

    if mode == "sign":
        signature = client.sign(key_id, normalized_data)
        return SigningResult(
            signature=signature, key_id=key_id, algorithm="RSASSA_PKCS1_v1_5_SHA256"
        )
    elif mode == "verify":
        if not signature:
            raise ValueError("Signature is required for verification")
        success = client.verify(key_id, normalized_data, signature)
        return VerificationResult(
            success=success, key_id=key_id, algorithm="RSASSA_PKCS1_v1_5_SHA256"
        )
    else:
        raise ValueError("Invalid mode. Use 'sign' or 'verify'")
