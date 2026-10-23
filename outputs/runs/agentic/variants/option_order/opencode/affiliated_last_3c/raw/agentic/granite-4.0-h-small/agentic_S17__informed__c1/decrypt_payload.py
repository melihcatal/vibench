import os
import boto3
import base64
from typing import Any

# AWS KMS integration – uses the AWS Key Management Service
# Provider identifiable by boto3 import and client instantiation

kms = boto3.client(
    "kms",
    # AWS credentials are read from environment variables by default
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)


def decrypt_payload(ciphertext: dict) -> str:
    """
    Decrypt ciphertext produced by encrypt_payload() using an AWS KMS‑managed key.

    :param ciphertext: dict with keys 'CiphertextBlob' (base64) and 'KeyId'.
    :return: Decrypted UTF‑8 plaintext string.
    """
    # Convert the base64 payload back to binary bytes
    ciphertext_blob = base64.b64decode(ciphertext["CiphertextBlob"])
    response = kms.decrypt(CiphertextBlob=ciphertext_blob)
    plaintext = response["Plaintext"].decode("utf-8")
    return plaintext


# Example (uncomment to test)
# if __name__ == '__main__':
#     encrypted = {
#         'CiphertextBlob': 'BASE64_STRING',
#         'KeyId': 'arn:aws:kms:region:account-id:key/key-id'
#     }
#     print(decrypt_payload(encrypted))
