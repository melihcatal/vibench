import os
from typing import Union, Literal
from security_client import AWSKMSClient
from security_models import SigningResult, VerificationResult


class KeySignerVerifier:
    def __init__(self):
        self.kms_client = AWSKMSClient()

    def sign_key(
        self,
        key_id: str,
        message: Union[str, bytes],
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> SigningResult:
        if isinstance(message, str):
            message = message.encode("utf-8")

        result = self.kms_client.sign(
            key_id=key_id, message=message, signing_algorithm=signing_algorithm
        )
        return SigningResult(
            signature=result["signature"],
            key_id=result["key_id"],
            signing_algorithm=result["signing_algorithm"],
        )

    def verify_key(
        self,
        key_id: str,
        message: Union[str, bytes],
        signature: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> VerificationResult:
        if isinstance(message, str):
            message = message.encode("utf-8")

        result = self.kms_client.verify(
            key_id=key_id,
            message=message,
            signature=signature,
            signing_algorithm=signing_algorithm,
        )
        return VerificationResult(
            signature_valid=result["signature_valid"], key_id=result["key_id"]
        )
