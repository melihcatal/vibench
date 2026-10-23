import os
import json
from typing import Dict, Any, Optional, Union
import boto3
from botocore.exceptions import ClientError
from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse, EncryptionAlgorithm


def encrypt_payload(
    plaintext: Union[str, bytes, Dict[str, Any]],
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> EncryptionResponse:
    client = SecurityClient()

    if not key_id:
        key_id = client.get_key_id()

    if not key_id:
        raise ValueError(
            "No key ID provided and AWS_KMS_KEY_ID environment variable not set"
        )

    if not client.validate_key_id(key_id):
        raise ValueError(f"Invalid key ID: {key_id}")

    encoded_plaintext = client.encode_payload(plaintext)

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        if algorithm == EncryptionAlgorithm.SYMMETRIC_DEFAULT:
            response = kms_client.encrypt(
                KeyId=key_id,
                Plaintext=encoded_plaintext,
                EncryptionContext=encryption_context or {},
            )
        else:
            response = kms_client.encrypt(
                KeyId=key_id,
                Plaintext=encoded_plaintext,
                EncryptionAlgorithm=algorithm.value,
                EncryptionContext=encryption_context or {},
            )

        return EncryptionResponse(
            ciphertext_blob=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_context=encryption_context,
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise RuntimeError(f"AWS KMS encryption failed: {error_code} - {error_msg}")


def encrypt_payload_from_request(request: EncryptionRequest) -> EncryptionResponse:
    return encrypt_payload(
        plaintext=request.plaintext,
        key_id=request.key_id,
        encryption_context=request.encryption_context,
        algorithm=request.algorithm,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        plaintext = sys.argv[1]
        key_id = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            result = encrypt_payload(plaintext, key_id)
            print(json.dumps(result.to_dict()))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
