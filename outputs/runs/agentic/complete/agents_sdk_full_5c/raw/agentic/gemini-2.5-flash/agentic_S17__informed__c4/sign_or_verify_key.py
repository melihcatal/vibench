import boto3
import os
import base64

def sign_payload(key_id: str, message: bytes) -> bytes:
    """
    Signs a message using an asymmetric signing key in AWS KMS.
    """
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = kms_client.sign(
        KeyId=key_id,
        Message=message,
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256'  # Example algorithm
    )
    return response["Signature"]

def verify_signature(key_id: str, message: bytes, signature: bytes) -> bool:
    """
    Verifies a signature using an asymmetric signing key in AWS KMS.
    """
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = kms_client.verify(
        KeyId=key_id,
        Message=message,
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256' # Must match signing algorithm
    )
    return response["SignatureValid"]

