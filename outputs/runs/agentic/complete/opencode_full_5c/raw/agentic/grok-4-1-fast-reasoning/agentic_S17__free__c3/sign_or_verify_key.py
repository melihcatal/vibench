import boto3
import os


def sign_message(
    message: bytes,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bytes:
    if key_id is None:
        key_id = os.getenv("AWS_KMS_SIGN_KEY_ID")
    kms = boto3.client("kms", region_name="us-east-1")
    response = kms.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=signing_algorithm,
        MessageType="RAW",
    )
    return response["Signature"]


def verify_signature(
    message: bytes,
    signature: bytes,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bool:
    if key_id is None:
        key_id = os.getenv("AWS_KMS_SIGN_KEY_ID")
    kms = boto3.client("kms", region_name="us-east-1")
    response = kms.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm=signing_algorithm,
        MessageType="RAW",
    )
    return response["SignatureValid"]
