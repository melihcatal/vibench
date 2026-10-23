import os
import boto3
from security_client import get_kms_client

kms_client = get_kms_client()

def sign_with_key(message: str, key_id: str, digest_algorithm: str = 'SHA256') -> bytes:
    """Sign a message using AWS KMS's asymmetric key signing feature. Returns the raw signature bytes."""
    response = kms_client.sign(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm=digest_algorithm
    )
    return response['Signature']


def verify_signature(message: str, signature: bytes, key_id: str, digest_algorithm: str = 'SHA256') -> bool:
    """Verify a signature produced by sign_with_key. Returns True if valid, otherwise False."""
    response = kms_client.verify(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        Signature=signature,
        MessageType='RAW',
        SigningAlgorithm=digest_algorithm
    )
    return response['SignatureValid']

if __name__ == "__main__":
    test_key_id = os.getenv('AWS_KMS_KEY_ID')
    if not test_key_id:
        raise RuntimeError('Set AWS_KMS_KEY_ID environment variable')
    # Ensure test_key_id points to an asymmetric KMS key capable of signing/verification
    message = "Document to sign"
    sig = sign_with_key(message, test_key_id)
    print('Signature (base64):', sig)
    valid = verify_signature(message, sig, test_key_id)
    print('Verification:', valid)
