import os
import json
from typing import Dict, Any, Optional, Union
import boto3
from botocore.exceptions import ClientError
import hashlib
from security_client import SecurityClient
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    SigningAlgorithm,
)


def sign_message(
    message: Union[str, bytes],
    key_id: str,
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256,
    message_type: str = "RAW",
) -> SignResponse:
    client = SecurityClient()

    if not client.validate_key_id(key_id):
        raise ValueError(f"Invalid key ID: {key_id}")

    if isinstance(message, str):
        message = message.encode("utf-8")

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        if message_type == "DIGEST":
            response = kms_client.sign(
                KeyId=key_id,
                Message=message,
                MessageType="DIGEST",
                SigningAlgorithm=algorithm.value,
            )
        else:
            response = kms_client.sign(
                KeyId=key_id,
                Message=message,
                MessageType="RAW",
                SigningAlgorithm=algorithm.value,
            )

        return SignResponse(
            signature=response["Signature"],
            key_id=response["KeyId"],
            algorithm=response["SigningAlgorithm"],
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise RuntimeError(f"AWS KMS signing failed: {error_code} - {error_msg}")


def verify_signature(
    message: Union[str, bytes],
    signature: bytes,
    key_id: str,
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256,
    message_type: str = "RAW",
) -> VerifyResponse:
    client = SecurityClient()

    if not client.validate_key_id(key_id):
        raise ValueError(f"Invalid key ID: {key_id}")

    if isinstance(message, str):
        message = message.encode("utf-8")

    kms_client = boto3.client("kms", region_name=client.region_name)

    try:
        if message_type == "DIGEST":
            response = kms_client.verify(
                KeyId=key_id,
                Message=message,
                MessageType="DIGEST",
                Signature=signature,
                SigningAlgorithm=algorithm.value,
            )
        else:
            response = kms_client.verify(
                KeyId=key_id,
                Message=message,
                MessageType="RAW",
                Signature=signature,
                SigningAlgorithm=algorithm.value,
            )

        return VerifyResponse(
            is_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            algorithm=response["SigningAlgorithm"],
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        raise RuntimeError(f"AWS KMS verification failed: {error_code} - {error_msg}")


def sign_message_with_digest(
    message: Union[str, bytes],
    key_id: str,
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256,
    hash_algorithm: str = "sha256",
) -> SignResponse:
    if isinstance(message, str):
        message = message.encode("utf-8")

    if hash_algorithm == "sha256":
        digest = hashlib.sha256(message).digest()
    elif hash_algorithm == "sha384":
        digest = hashlib.sha384(message).digest()
    elif hash_algorithm == "sha512":
        digest = hashlib.sha512(message).digest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    return sign_message(digest, key_id, algorithm, "DIGEST")


def verify_signature_with_digest(
    message: Union[str, bytes],
    signature: bytes,
    key_id: str,
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256,
    hash_algorithm: str = "sha256",
) -> VerifyResponse:
    if isinstance(message, str):
        message = message.encode("utf-8")

    if hash_algorithm == "sha256":
        digest = hashlib.sha256(message).digest()
    elif hash_algorithm == "sha384":
        digest = hashlib.sha384(message).digest()
    elif hash_algorithm == "sha512":
        digest = hashlib.sha512(message).digest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    return verify_signature(digest, signature, key_id, algorithm, "DIGEST")


def sign_message_from_request(request: SignRequest) -> SignResponse:
    return sign_message(
        message=request.message,
        key_id=request.key_id,
        algorithm=request.algorithm,
        message_type=request.message_type,
    )


def verify_signature_from_request(request: VerifyRequest) -> VerifyResponse:
    return verify_signature(
        message=request.message,
        signature=request.signature,
        key_id=request.key_id,
        algorithm=request.algorithm,
        message_type=request.message_type,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 3:
        action = sys.argv[1]
        key_id = sys.argv[2]
        message = sys.argv[3]

        try:
            if action == "sign":
                result = sign_message(message, key_id)
                print(json.dumps(result.to_dict()))
            elif action == "verify" and len(sys.argv) > 4:
                signature_hex = sys.argv[4]
                signature = bytes.fromhex(signature_hex)
                result = verify_signature(message, signature, key_id)
                print(json.dumps(result.to_dict()))
            else:
                print(
                    "Usage: sign_or_verify_key.py <sign|verify> <key_id> <message> [signature_hex]",
                    file=sys.stderr,
                )
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
