import os
import json
from typing import Dict, Any, Optional, Union
import boto3
from botocore.exceptions import ClientError
from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(
    ciphertext_blob: bytes, encryption_context: Optional[Dict[str, str]] = None
) -> DecryptionResponse:
    client = SecurityClient()

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob, EncryptionContext=encryption_context or {}
        )

        return DecryptionResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        if error_code == "InvalidCiphertextException":
            raise ValueError(f"Invalid ciphertext: {error_msg}")
        elif error_code == "IncorrectKeyException":
            raise ValueError(f"Incorrect key for decryption: {error_msg}")
        elif error_code == "InvalidKeyUsageException":
            raise ValueError(f"Key cannot be used for decryption: {error_msg}")
        else:
            raise RuntimeError(f"AWS KMS decryption failed: {error_code} - {error_msg}")


def decrypt_payload_from_request(request: DecryptionRequest) -> DecryptionResponse:
    return decrypt_payload(
        ciphertext_blob=request.ciphertext_blob,
        encryption_context=request.encryption_context,
    )


def decrypt_and_decode(
    ciphertext_blob: bytes, encryption_context: Optional[Dict[str, str]] = None
) -> Union[str, Dict[str, Any]]:
    response = decrypt_payload(ciphertext_blob, encryption_context)
    client = SecurityClient()
    return client.decode_payload(response.plaintext)


def decrypt_hex_payload(
    ciphertext_hex: str, encryption_context: Optional[Dict[str, str]] = None
) -> DecryptionResponse:
    ciphertext_blob = bytes.fromhex(ciphertext_hex)
    return decrypt_payload(ciphertext_blob, encryption_context)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        ciphertext_hex = sys.argv[1]
        try:
            result = decrypt_hex_payload(ciphertext_hex)
            print(json.dumps(result.to_dict()))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
