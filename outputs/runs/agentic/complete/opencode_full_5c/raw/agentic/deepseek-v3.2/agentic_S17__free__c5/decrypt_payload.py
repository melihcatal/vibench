import os
import base64
import boto3
from botocore.exceptions import ClientError


def decrypt_payload(ciphertext: str, key_id: str = None) -> str:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Args:
        ciphertext: Base64-encoded ciphertext
        key_id: AWS KMS key ID or alias (optional, will be extracted from ciphertext)

    Returns:
        Decrypted plaintext string
    """
    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    try:
        ciphertext_blob = base64.b64decode(ciphertext)

        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob,
            KeyId=key_id if key_id else None,
            EncryptionAlgorithm="SYMMETRIC_DEFAULT",
        )

        plaintext = response["Plaintext"].decode("utf-8")

        return plaintext
    except ClientError as e:
        raise Exception(f"AWS KMS decryption failed: {e}")


if __name__ == "__main__":
    test_ciphertext = "AQICAHh...example...ciphertext"
    try:
        result = decrypt_payload(test_ciphertext)
        print(f"Decrypted text: {result}")
    except Exception as e:
        print(f"Decryption failed: {e}")
