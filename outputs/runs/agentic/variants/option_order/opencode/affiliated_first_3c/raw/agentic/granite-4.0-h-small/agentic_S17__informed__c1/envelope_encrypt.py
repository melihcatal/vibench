import os
from security_client import KmsEncryptRequest, get_aws_kms_client

# Configure KMS client using AWS credentials
_kms_client = get_aws_kms_client()


def envelope_encrypt(plaintext: bytes) -> dict:
    """Envelopes a plaintext payload using an AWS-managed data key.

    Steps:
    1. Generate a data key using the specified CMK
    2. Encrypt the plaintext with the plaintext data key
    3. Return the encrypted data key (ciphertext blob) and the encrypted payload
    """
    # Generate a data key (ENCRYPT/DECRYPT) with AWS KMS
    key_id = os.getenv(
        "AWS_KMS_KEY_ID"
    )  # environment variable with target CMK ARN/alias
    response = _kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    data_key = response["Plaintext"]  # binary AES-256 key
    encrypted_data_key = response["CiphertextBlob"]
    # Encrypt the payload with the plaintext data key
    encrypted_payload = _kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)[
        "CiphertextBlob"
    ]
    return {
        "EncryptedDataKey": encrypted_data_key,
        "EncryptedPayload": encrypted_payload,
        "KeyId": key_id,
    }


def envelope_decrypt(encrypted_data_key: bytes, encrypted_payload: bytes) -> bytes:
    """Decrypts an envelope-encrypted payload.

    1. Decrypts the encrypted data key to retrieve the plaintext AES key
    2. Uses the plaintext key to decrypt the ciphertext payload
    """
    # Decrypt the data key
    decrypted_data_key = _kms_client.decrypt(CiphertextBlob=encrypted_data_key)[
        "Plaintext"
    ]
    # Decrypt the payload with the recovered key
    plaintext = _kms_client.decrypt(CiphertextBlob=encrypted_payload)["Plaintext"]
    return plaintext
