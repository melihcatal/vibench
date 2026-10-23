import os
from typing import Dict, Optional
import boto3
from security_client import get_kms_client
from hashlib import sha256

def sign_payload(message: str, key_id: str = None) -> Dict[str, str]:
    """Signs a message using an asymmetric key in AWS KMS."""
    kms_client = get_kms_client()
    if key_id is None:
        key_id = os.environ.get("KMS_KEY_ID")
        if not key_id:
            raise ValueError("KMS_KEY_ID environment variable or key_id parameter must be set.")

    message_bytes = message.encode('utf-8')
    digest = sha256(message_bytes).digest()

    try:
        response = kms_client.sign(
            KeyId=key_id,
            Message=digest,
            MessageType='DIGEST',
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Common signing algorithm
        )
        return {
            "Signature": response['Signature'].hex(),
            "SigningAlgorithm": response['SigningAlgorithm'],
            "KeyId": response['KeyId']
        }
    except Exception as e:
        raise RuntimeError(f"Failed to sign message with KMS: {e}")

def verify_signature(message: str, signature_hex: str, key_id: str = None, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA256') -> bool:
    """Verifies a signature using an asymmetric key in AWS KMS."""
    kms_client = get_kms_client()
    if key_id is None:
        key_id = os.environ.get("KMS_KEY_ID")
        if not key_id:
            raise ValueError("KMS_KEY_ID environment variable or key_id parameter must be set.")

    message_bytes = message.encode('utf-8')
    digest = sha256(message_bytes).digest()
    signature = bytes.fromhex(signature_hex)

    try:
        response = kms_client.verify(
            KeyId=key_id,
            Message=digest,
            MessageType='DIGEST',
            Signature=signature,
            SigningAlgorithm=signing_algorithm
        )
        return response['SignatureValid']
    except Exception as e:
        print(f"Error during signature verification with KMS: {e}")
        return False