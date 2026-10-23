import os
from typing import Union, Literal
from security_client import AWSKMSClient
from security_models import SigningResult, VerificationResult


def sign_or_verify_key(
    message: Union[str, bytes],
    operation: Literal["sign", "verify"],
    signature: bytes = None,
) -> Union[SigningResult, VerificationResult]:
    if isinstance(message, str):
        message = message.encode("utf-8")

    client = AWSKMSClient()

    if operation == "sign":
        result = client.sign(message)
        return SigningResult(
            signature=result["signature"],
            key_id=result["key_id"],
            signing_algorithm=result["signing_algorithm"],
        )
    elif operation == "verify":
        if not signature:
            raise ValueError("Signature is required for verification")
        result = client.verify(message, signature)
        return VerificationResult(
            signature_valid=result["signature_valid"], key_id=result["key_id"]
        )
    else:
        raise ValueError("Operation must be either 'sign' or 'verify'")
