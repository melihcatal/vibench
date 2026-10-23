import boto3
import os
import base64

def sign_payload(key_id: str, message: str) -> bytes:
    """
    Signs a message using an asymmetric KMS key.

    Args:
        key_id: The KMS key ID or ARN configured for signing.
        message: The message to sign.

    Returns:
        The signature blob.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    response = kms_client.sign(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Example algorithm, depends on key spec
    )
    return response['Signature']

def verify_signature(key_id: str, message: str, signature: bytes) -> bool:
    """
    Verifies a signature using an asymmetric KMS key.

    Args:
        key_id: The KMS key ID or ARN used for signing.
        message: The original message.
        signature: The signature to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    response = kms_client.verify(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Example algorithm, must match signing
    )
    return response['SignatureValid']
