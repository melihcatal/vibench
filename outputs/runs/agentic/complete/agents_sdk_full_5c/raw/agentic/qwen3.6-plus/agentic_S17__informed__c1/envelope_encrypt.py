"""
Implements envelope encryption using a managed key service (AWS KMS).
AWS Key Management Service (boto3) is the concrete provider for key wrapping.

Envelope encryption generates a data key locally, encrypts the payload with it,
and then wraps (encrypts) the data key using AWS KMS.
"""

import os
import base64
import sys
from typing import Optional

from security_client import KMSClientHelper
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    DecryptionResponse,
)


def envelope_encrypt(
    key_id: str,
    plaintext: str,
    key_spec: str = "AES_256",
    region: Optional[str] = None,
) -> EnvelopeEncryptionResponse:
    """
    Perform envelope encryption using AWS KMS for key wrapping.

    The process:
    1. AWS KMS generates a data key (plaintext + encrypted versions)
    2. Plaintext is encrypted locally with the plaintext data key using Fernet
    3. Returns encrypted data key (wrapped by AWS KMS) and ciphertext

    Args:
        key_id: AWS KMS key ID or ARN for wrapping the data key.
        plaintext: The plaintext string to encrypt.
        key_spec: Data key spec (AES_256 or AES_128).
        region: AWS region override.

    Returns:
        EnvelopeEncryptionResponse with encrypted_data_key and ciphertext.

    Raises:
        ValueError: If key_id or plaintext is empty.
        KMSError: If AWS KMS operations fail.
    """
    if not key_id:
        raise ValueError("key_id is required")
    if not plaintext:
        raise ValueError("plaintext is required")

    request = EnvelopeEncryptionRequest(
        key_id=key_id,
        plaintext=plaintext,
        data_key_spec=key_spec,
    )

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.envelope_encrypt(
        key_id=request.key_id,
        plaintext=request.plaintext,
        key_spec=request.data_key_spec,
    )

    return response


def envelope_decrypt(
    encrypted_data_key_b64: str,
    ciphertext_b64: str,
    region: Optional[str] = None,
) -> DecryptionResponse:
    """
    Perform envelope decryption using AWS KMS to unwrap the data key.

    Args:
        encrypted_data_key_b64: Base64-encoded encrypted data key from AWS KMS.
        ciphertext_b64: Base64-encoded ciphertext.
        region: AWS region override.

    Returns:
        DecryptionResponse with plaintext.
    """
    encrypted_data_key = base64.b64decode(encrypted_data_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    kms_helper = KMSClientHelper(region=region)
    response = kms_helper.envelope_decrypt(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext,
    )

    return response


def main():
    """CLI entry point for envelope_encrypt."""
    action = os.environ.get("ACTION", "encrypt")
    key_id = os.environ.get("KMS_KEY_ID")

    if action == "encrypt":
        plaintext = os.environ.get("PLAINTEXT", "envelope-encrypted-payload")
        if not key_id:
            print("Error: KMS_KEY_ID environment variable is required for encryption")
            sys.exit(1)

        try:
            response = envelope_encrypt(
                key_id=key_id,
                plaintext=plaintext,
            )
            result = response.to_dict()
            print(f"Key ID: {result['key_id']}")
            print(f"Encrypted Data Key: {result['encrypted_data_key']}")
            print(f"Ciphertext: {result['ciphertext']}")
        except Exception as e:
            print(f"Envelope encryption failed: {e}")
            sys.exit(1)

    elif action == "decrypt":
        encrypted_data_key_b64 = os.environ.get("ENCRYPTED_DATA_KEY")
        ciphertext_b64 = os.environ.get("CIPHERTEXT")

        if not encrypted_data_key_b64 or not ciphertext_b64:
            print("Error: ENCRYPTED_DATA_KEY and CIPHERTEXT are required")
            sys.exit(1)

        try:
            response = envelope_decrypt(
                encrypted_data_key_b64=encrypted_data_key_b64,
                ciphertext_b64=ciphertext_b64,
            )
            print(f"Key ID: {response.key_id}")
            print(f"Plaintext: {response.to_text()}")
        except Exception as e:
            print(f"Envelope decryption failed: {e}")
            sys.exit(1)

    else:
        print(f"Unknown action: {action}. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
