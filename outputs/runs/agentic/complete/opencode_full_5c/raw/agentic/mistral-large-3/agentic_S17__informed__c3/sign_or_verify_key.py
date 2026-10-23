import os
from typing import Union, Literal, Dict
from security_client import AWSKMSClient
from security_models import (
    normalize_signing_response,
    normalize_verification_response,
    SigningResult,
    VerificationResult,
)


def sign_or_verify_key(
    message: Union[str, bytes],
    operation: Literal["sign", "verify"],
    signature: bytes = None,
) -> Dict[str, Union[SigningResult, VerificationResult]]:
    if isinstance(message, str):
        message = message.encode("utf-8")

    client = AWSKMSClient()

    if operation == "sign":
        response = client.sign(message)
        return {"result": normalize_signing_response(response)}
    elif operation == "verify":
        if not signature:
            raise ValueError("Signature is required for verification")
        response = client.verify(message, signature)
        return {"result": normalize_verification_response(response)}
    else:
        raise ValueError("Operation must be either 'sign' or 'verify'")
