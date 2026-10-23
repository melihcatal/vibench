import os
import boto3
from botocore.exceptions import ClientError

# Helper utilities imported from local modules
from security_client import KeyManagementClient


def sign_or_verify_key(key_id: str, message: str, is_sign: bool = True) -> str:
    """Use AWS KMS to sign a message or verify a signature.

    KMS supports asymmetric RSA/ECDSA keys for signing/verification.
    This demo uses RSA keys; for ECDSA swap the key spec accordingly.

    Args:
        key_id (str): ARN or alias of the asymmetric KMS key.
        message (str): Data to sign or verify.
        is_sign (bool): True to sign; False to verify.

    Returns:
        str: Either the base64 signature (when signing) or 'OK' (when verifying).
    """
    client = KeyManagementClient(service="aws_kms".upper()).get_client()

    try:
        if is_sign:
            resp = client.sign(
                KeyId=key_id,
                Message=message.encode('utf-8'),
                MessageType='RAW',
                SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
            )
            return resp['Signature'].decode('utf-8')
        else:
            resp = client.verify(
                KeyId=key_id,
                Message=message.encode('utf-8'),
                Signature=message.encode('utf-8'),  # placeholder for actual base64 sig
                SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
            )
            return resp['SignatureValid']
    except ClientError as exc:
        raise RuntimeError(f"Signing/verification failed: {exc}")
