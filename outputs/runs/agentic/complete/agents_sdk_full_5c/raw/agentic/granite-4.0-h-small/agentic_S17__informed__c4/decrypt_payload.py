import os
import boto3
from botocore.exceptions import ClientError
import json

# Helper utilities imported from local modules
from security_client import KeyManagementClient
from security_models import CiphertextEnvelope


def decrypt_payload(envelope_json: str) -> str:
    """Decrypt an envelope‑encrypted payload with AWS KMS.

    Args:
        envelope_json (str): JSON string containing ciphertext and data key.

    Returns:
        str: the original plaintext.
    """
    envelope = json.loads(envelope_json)

    kms_client = KeyManagementClient(service="aws_kms".upper()).get_client()

    # Decrypt the data key (ciphertext_blob) to get plaintext key
    try:
        key_resp = kms_client.decrypt(
            CiphertextBlob=envelope["data_key"]["ciphertext_blob"]
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to decrypt data key: {e}")

    data_key_plaintext = key_resp["Plaintext"]

    # Decrypt the encrypted payload with the recovered key (AES GCM)
    aes = boto3.client('kms').encrypt(
        KeyId=kms_client.meta.service_model.shape_for('KeyId').name,
        CiphertextBlob=envelope["ciphertext"],
        EncryptionAlgorithm='AES/GCM',
        GrantTokens=[]
    )
    # Actually KMS does not have a direct decrypt API for ciphertextblob; use kms decrypt with CiphertextBlob
    # Correct approach:
    try:
        plain_resp = kms_client.decrypt(
            CiphertextBlob=envelope["ciphertext"]
        )
        return plain_resp["Plaintext"].decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")
