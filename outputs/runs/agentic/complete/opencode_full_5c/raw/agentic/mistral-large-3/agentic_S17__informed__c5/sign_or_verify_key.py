import os
from security_client import AWSKMSClient
from security_models import (
    SignRequest,
    VerifyRequest,
    normalize_sign_response,
    normalize_verify_response,
)


def sign_or_verify_key(
    key_id: str, message: str, action: str = "sign", signature_hex: str = None
) -> dict:
    """
    Signs or verifies a message using AWS KMS.

    Args:
        key_id: AWS KMS key ID or ARN.
        message: Message to sign or verify.
        action: 'sign' or 'verify'.
        signature_hex: Hex-encoded signature for verification.

    Returns:
        Dictionary containing signature or verification result.
    """
    client = AWSKMSClient()
    message_bytes = message.encode("utf-8")

    if action == "sign":
        sign_request = SignRequest(key_id=key_id, message=message_bytes)
        response = client.sign(
            key_id=sign_request.key_id,
            message=sign_request.message,
            signing_algorithm=sign_request.signing_algorithm,
        )
        normalized_response = normalize_sign_response(response)
        return {
            "signature": normalized_response.signature.hex(),
            "key_id": normalized_response.key_id,
            "signing_algorithm": normalized_response.signing_algorithm,
        }
    elif action == "verify":
        if not signature_hex:
            raise ValueError("Signature is required for verification.")
        signature = bytes.fromhex(signature_hex)
        verify_request = VerifyRequest(
            key_id=key_id, message=message_bytes, signature=signature
        )
        response = client.verify(
            key_id=verify_request.key_id,
            message=verify_request.message,
            signature=verify_request.signature,
            signing_algorithm=verify_request.signing_algorithm,
        )
        normalized_response = normalize_verify_response(response)
        return {
            "signature_valid": normalized_response.signature_valid,
            "key_id": normalized_response.key_id,
        }
    else:
        raise ValueError("Action must be 'sign' or 'verify'.")
