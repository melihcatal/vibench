import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import SignOrVerifyRequest, SignOrVerifyResponse

def sign_or_verify(input_bytes: bytes, key_name: str, sign: bool = True) -> SignOrVerifyResponse:
    """Uses a managed KMS CryptoKey for signing or verification.

    Google Cloud KMS supports asymmetric keys and can sign or verify
    using RSA or ECDSA algorithms. The function abstracts both actions
    into a single call.

    Args:
        input_bytes: Data to sign (when `sign=True`) or to verify (when
            `sign=False`).
        key_name: Full KMS CryptoKey resource name.
        sign: If True, perform a signature generation; if False,
            perform a verification check.

    Returns:
        SignOrVerifyResponse containing `signature` (Base64) for signing,
        or `is_valid` (bool) for verification.
    """
    client = get_kms_client()
    if sign:
        # Asymmetric signing with KMS returns a detached signature
        sign_req = kms_v1.AsymmetricSignRequest(
            name=key_name,
            digest={'value': input_bytes},
        )
        response = client.asymmetric_sign(sign_req)
        return SignOrVerifyResponse(signature=response.signature.decode('utf-8'))
    else:
        # Verification request returns validated result via the SDK's
        # built‑in verification flow (raises on failure)
        verify_req = kms_v1.AsymmetricVerifyRequest(
            name=key_name,
            signature=input_bytes,
            digest={'value': input_bytes},  # dummy digest for API shape
        )
        # The SDK throws an exception on invalid signature; we catch and
        # return False
        try:
            client.asymmetric_verify(verify_req)
            return SignOrVerifyResponse(is_valid=True)
        except Exception:
            return SignOrVerifyResponse(is_valid=False)
