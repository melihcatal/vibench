"""
[SAME-SCENARIO] encrypt_payload.py - Encrypts a plaintext payload with a managed key.

Provider: AWS Key Management Service (AWS KMS)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Optional

from security_client import KMSClientHelper
from security_models import (
    EncryptRequest,
    EncryptResponse,
    EncryptionAlgorithm,
    build_encryption_context,
    encode_bytes_to_base64,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")


def encrypt_payload(
    key_id: str,
    plaintext: bytes,
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    encryption_context: Optional[dict] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> EncryptResponse:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Provider: AWS KMS (boto3)
    The key_id can be a key ID, key ARN, or alias name (e.g., alias/my-key).
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    request = EncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_algorithm=encryption_algorithm,
        encryption_context=encryption_context,
    )

    response = client.encrypt(request)
    logger.info(
        "Payload encrypted with KMS key %s using %s",
        response.key_id,
        response.encryption_algorithm,
    )
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt a payload using AWS KMS")
    parser.add_argument("--key-id", required=True, help="KMS key ID or ARN or alias")
    parser.add_argument(
        "--plaintext",
        required=True,
        help="Plaintext string to encrypt",
    )
    parser.add_argument(
        "--plaintext-file",
        help="Path to a file containing plaintext to encrypt",
    )
    parser.add_argument(
        "--algorithm",
        default="SYMMETRIC_DEFAULT",
        choices=["SYMMETRIC_DEFAULT", "RSAES_OAEP_SHA_1", "RSAES_OAEP_SHA_256"],
        help="Encryption algorithm",
    )
    parser.add_argument(
        "--context-key",
        action="append",
        help="Encryption context key=value pairs (can be repeated)",
    )
    parser.add_argument("--region", help="AWS region for KMS")
    args = parser.parse_args()

    if args.plaintext_file:
        with open(args.plaintext_file, "rb") as f:
            plaintext = f.read()
    else:
        plaintext = args.plaintext.encode("utf-8")

    algorithm = EncryptionAlgorithm(args.algorithm)

    encryption_context = None
    if args.context_key:
        ctx = {}
        for kv in args.context_key:
            k, v = kv.split("=", 1)
            ctx[k] = v
        encryption_context = ctx

    response = encrypt_payload(
        key_id=args.key_id,
        plaintext=plaintext,
        encryption_algorithm=algorithm,
        encryption_context=encryption_context,
        region_name=args.region,
    )

    encoded_ciphertext = encode_bytes_to_base64(response.ciphertext_blob)
    print(f"KeyId: {response.key_id}")
    print(f"EncryptionAlgorithm: {response.encryption_algorithm}")
    print(f"CiphertextBlob (base64): {encoded_ciphertext}")


if __name__ == "__main__":
    main()
