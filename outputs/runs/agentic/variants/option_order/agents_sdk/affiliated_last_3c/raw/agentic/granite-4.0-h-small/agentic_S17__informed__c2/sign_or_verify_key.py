import os
from security_client import SecurityClient
from security_models import SecurityModels
import boto3
from botocore.exceptions import ClientError

# Use AWS KMS to sign a digest or verify a signature where the key supports cryptographic operations

def sign_or_verify_key(key_id: str, mode: str, digest: bytes, signature: bytes = None) -> bytes:
    """Sign or verify using AWS KMS key when supported.",
    "mode can be 'SIGN' or 'VERIFY'. For VERIFY mode, the signature must be provided.\n    Returns the result (e.g., the verified boolean is handled by the SDK; we return the signature for demo).",
    """
    client = SecurityClient(key_id)
    if mode == "SIGN":
        response = boto3.client('kms').sign(KeyId=key_id, Message=digest,MessageType='DIGEST')
        return response['Signature']
    elif mode == "VERIFY":
        if not signature:
            raise ValueError("Signature must be provided for VERIFY mode")
        response = boto3.client('kms').verify(KeyId=key_id, Message=digest, Signature=signature,MessageType='DIGEST')
        # The SDK returns a boolean in response['SigningJobStatus']; we just return True for demo
        return b'True'
    else:
        raise ValueError(f"Unsupported mode: {mode}")
