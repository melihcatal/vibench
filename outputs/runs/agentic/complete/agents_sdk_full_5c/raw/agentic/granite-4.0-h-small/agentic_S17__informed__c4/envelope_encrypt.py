import json
import boto3
from botocore.exceptions import ClientError

# Helper utilities imported from local modules
from security_client import KeyManagementClient
from security_models import PlaintextEnvelope


def envelope_encrypt(plaintext: str, key_id: str) -> str:
    """Perform envelope encryption using AWS KMS.

    Generates a data key, encrypts the plaintext with the plaintext data key,
    and returns a JSON envelope containing the ciphertext and encrypted data key.

    Args:
        plaintext (str): The clear text to encrypt.
        key_id (str): ARN or alias of the KMS key to use for data key generation.

    Returns:
        str: JSON representation of the envelope.
    """
    client = KeyManagementClient(service="aws_kms".upper()).get_client()

    # 1️⃣ Generate a data key (plaintext + ciphertext blob)
    try:
        data_key = client.generate_data_key(
            KeyId=key_id,
            KeySpec="AES_256"
        )
    except ClientError as exc:
        raise RuntimeError(f"Data key generation failed: {exc}")

    plaintext_key = data_key["Plaintext"]
    encrypted_key_blob = data_key["CiphertextBlob"]

    # 2️⃣ Encrypt the plaintext payload with the plaintext data key (AES/GCM)
    try:
        encrypted_payload = client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode('utf-8'),
            EncryptionAlgorithm="AES/GCM"
        )
    except ClientError as exc:
        raise RuntimeError(f"Payload encryption failed: {exc}")

    # 3️⃣ Assemble envelope (JSON string for transport)
    envelope = PlaintextEnvelope(
        ciphertext=encrypted_payload["CiphertextBlob"],
        data_key=dict(
            # Store encrypted key and its plaintext hex representation for demo purposes
            ciphertext_blob=encrypted_key_blob,
            plaintext_key=plaintext_key.hex()
        )
    )
    return json.dumps(envelope)
