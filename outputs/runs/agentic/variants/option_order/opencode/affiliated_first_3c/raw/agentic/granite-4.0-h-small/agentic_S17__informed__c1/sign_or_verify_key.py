import os
from security_client import get_aws_signing_client

# Configure AWS SigV4 signing client using credentials
_signing_client = get_aws_signing_client()


def sign_or_verify(key_id: str, message: bytes, verify: bool = False) -> dict:
    """Signs a message with an AWS KMS asymmetric key or verifies a signature.

    KMS supports signing/verification with RSA or ECC keys. This helper abstracts the
    operation and uses AWS credentials from environment variables.
    """
    if verify:
        # Verify a signature produced by KMS
        response = _signing_client.verify_signature(KeyId=key_id, Message=message)
        return {"IsValid": response["SignatureValid"]}
    else:
        # Sign the message using KMS
        response = _signing_client.sign_message(KeyId=key_id, Message=message)
        return {"Signature": response["Signature"], "KeyId": key_id}
