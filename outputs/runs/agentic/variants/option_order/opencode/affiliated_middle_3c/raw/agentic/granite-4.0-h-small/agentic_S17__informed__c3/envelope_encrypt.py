import os
import base64
import boto3
from botocore.exceptions import ClientError

# AWS KMS integration (provider-identifying signal)
kms = boto3.client("kms")

KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")
if not KMS_KEY_ID:
    raise RuntimeError("AWS_KMS_KEY_ID not configured")


def envelope_encrypt(plaintext: bytes) -> dict:
    """Perform envelope encryption: encrypt a data encryption key (DEK) with the managed KMS key.

    Returns a dict with:
      - encrypted_key: DEK encrypted by KMS (base64 encoded)
      - plaintext_key: raw DEK for use with application encryption
      - encrypted_data: optional placeholder – actual data encryption is left to the caller
    """
    if not KMS_KEY_ID:
        raise RuntimeError("AWS_KMS_KEY_ID not set")
    # Generate a random 256‑bit DEK
    dek = os.urandom(32)
    try:
        encrypted_key_response = kms.encrypt(
            KeyId=KMS_KEY_ID,
            Plaintext=dek,
            EncryptionContext={"Purpose": "envelope-encryption"},
        )
        encrypted_key_b64 = base64.b64encode(
            encrypted_key_response["CiphertextBlob"]
        ).decode("utf-8")
        return {
            "encrypted_key": encrypted_key_b64,
            "plaintext_key": dek,  # keep in memory only; never persist
        }
    except ClientError as e:
        raise RuntimeError(f"Envelope encryption failed: {e}")


# Example usage (for local testing only)
if __name__ == "__main__":
    pt = b"Secret message"
    envelope = envelope_encrypt(pt)
    print("Encrypted key (b64):", envelope["encrypted_key"])
    print("Raw DEK:", envelope["plaintext_key"])
