import os
import boto3
from typing import Any

# AWS KMS integration – uses the AWS Key Management Service
# Provider identifiable by boto3 import and client instantiation

kms = boto3.client(
    "kms",
    # AWS credentials are read from environment variables by default
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)


def sign_message(message: str, key_id: str) -> dict:
    """
    Sign a message using an asymmetric AWS KMS customer master key (CMK).

    :param message: The UTF‑8 plaintext to sign.
    :param key_id: ARN or alias of a symmetric or asymmetric CMK capable of signing.
    :return: Dictionary with the signature (base64) and key ID used.
    """
    plaintext_bytes = message.encode("utf-8")
    response = kms.sign(KeyId=key_id, Message=plaintext_bytes, MessageType="RAW")
    signature_b64 = base64.b64encode(response["Signature"]).decode("utf-8")
    return {"Signature": signature_b64, "KeyId": key_id}


def verify_signature(message: str, signature: str, key_id: str) -> bool:
    """
    Verify a signature produced by sign_message() using the same CMK.

    :param message: Original plaintext that was signed.
    :param signature: Base64 signature returned from sign_message().
    :param key_id: ARN/alias of the same CMK used for signing.
    :return: True if verification succeeds, False otherwise.
    """
    plaintext_bytes = message.encode("utf-8")
    signature_bytes = base64.b64decode(signature)
    try:
        response = kms.verify(
            KeyId=key_id,
            Message=plaintext_bytes,
            Signature=signature_bytes,
            MessageType="RAW",
        )
    except kms.exceptions.InvalidCiphertextException:
        return False
    return response["SigningAlgorithm"] == "RSASSA_PKCS1_V1_5_SHA_256"  # example check


# Example usage (uncomment to test)
# if __name__ == '__main__':
#     sig = sign_message('Hello, sign!', 'alias/my-signing-key')
#     print('Signature:', sig)
#     ok = verify_signature('Hello, sign!', sig['Signature'], 'alias/my-signing-key')
#     print('Verification OK?', ok)
