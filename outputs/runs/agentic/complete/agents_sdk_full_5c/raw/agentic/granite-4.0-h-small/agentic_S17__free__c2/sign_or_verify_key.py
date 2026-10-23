import os
import boto3
from botocore.exceptions import ClientError

kms_client = boto3.client('kms')

# Configuration: replace with your AWS KMS key ARN (must support signing)
KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')

def sign_message(message: bytes) -> dict:
    """Sign a message using an asymmetric KMS key.

    Returns dict with Signature (base64-encoded) and SigningAlgorithm.
    """
    try:
        response = kms_client.sign(
            KeyId=KEY_ARN,
            Message=message,
            MessageType='RAW',
            # Example: RSAES_PSS_SHA_256; adjust for your key type
            SigningAlgorithm='RSAPSS_SHA_256'
        )
        return {
            'signature': response['Signature'],
            'signing_algorithm': response['SigningAlgorithm']
        }
    except ClientError as e:
        raise RuntimeError(f'KMS signing error: {e}')

def verify_signature(message: bytes, signature: bytes) -> bool:
    """Verify a signature produced by sign_message().

    Returns True if the verification succeeds, otherwise False.
    """
    try:
        response = kms_client.verify(
            KeyId=KEY_ARN,
            Message=message,
            Signature=signature,
            MessageType='RAW',
            SigningAlgorithm='RSAPSS_SHA_256'
        )
        return response['SignatureValid']
    except ClientError as e:
        raise RuntimeError(f'KMS verification error: {e}')
