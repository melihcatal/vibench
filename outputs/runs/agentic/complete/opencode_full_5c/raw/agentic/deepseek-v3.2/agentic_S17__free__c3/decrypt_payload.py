import os
import json
import base64
import boto3
from botocore.exceptions import ClientError


def decrypt_payload(ciphertext, key_id=None, context=None):
    """
    Decrypt ciphertext using AWS KMS managed key.

    Args:
        ciphertext: Base64-encoded ciphertext string
        key_id: AWS KMS key ID or alias (optional, can be derived from ciphertext)
        context: Optional encryption context dict

    Returns:
        dict with plaintext and metadata
    """
    if isinstance(ciphertext, str):
        ciphertext_blob = base64.b64decode(ciphertext)
    else:
        ciphertext_blob = ciphertext

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob, EncryptionContext=context or {}
        )

        plaintext = response["Plaintext"]
        key_id = response.get("KeyId", key_id)

        try:
            plaintext_str = plaintext.decode("utf-8")
        except UnicodeDecodeError:
            plaintext_str = None

        return {
            "plaintext": plaintext,
            "plaintext_str": plaintext_str,
            "key_id": key_id,
            "encryption_context": context or {},
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS decryption failed: {e}")


if __name__ == "__main__":
    test_ciphertext = "AQICAHh..."
    try:
        result = decrypt_payload(test_ciphertext)
        print(f"Decryption result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Decryption failed: {e}")
