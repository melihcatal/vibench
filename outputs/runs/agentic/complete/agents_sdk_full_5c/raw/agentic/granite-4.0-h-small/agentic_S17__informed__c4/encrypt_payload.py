import os
import boto3
from botocore.exceptions import ClientError

# Helper utilities imported from local modules
from security_client import KeyManagementClient
from security_models import PlaintextEnvelope


def encrypt_payload(plaintext: str, key_id: str) -> str:
    """Encrypt a plaintext payload using AWS KMS envelope encryption.

    Args:
        plaintext (str): the data to encrypt.
        key_id (str): ARN or alias of the KMS data key.

    Returns:
        str: envelope-encrypted ciphertext (JSON string).
    """
    kms_client = KeyManagementClient(service="aws_kms".upper()).get_client()

    # Generate a data key
    try:
        data_key_resp = kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec="AES_256"
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to generate data key: {e}")

    plaintext_key = data_key_resp["Plaintext"]
    ciphertext_blob = data_key_resp["CiphertextBlob"]

    # Encrypt payload with the plaintext data key (AES GCM)
    aes = boto3.client('kms').encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8'),
        EncryptionAlgorithm='AES/GCM'
    )
    encrypted_payload = aes["CiphertextBlob"]

    # Build envelope format
    envelope = {
        "ciphertext": encrypted_payload,
        "data_key": {
            "ciphertext_blob": ciphertext_blob,
            "plaintext_key": plaintext_key.hex()
        }
    }
    return str(envelope)
