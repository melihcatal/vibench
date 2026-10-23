"""
[SAME-SCENARIO] decrypt_payload.py - Decrypts a ciphertext payload with a managed key.

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
    DecryptRequest,
    DecryptResponse,
    EncryptionAlgorithm,
    build_encryption_context,
    decode_base64_to_bytes,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")


def decrypt_payload(
    ciphertext_blob: bytes,
    key_id: Optional[str] = None,
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    encryption_context: Optional[dict] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> DecryptResponse:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Provider: AWS KMS (boto3)
    The key_id is optional if the ciphertext blob already contains key identification.
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    request = DecryptRequest(
        key_id=key_id,
        ciphertext_blob=ciphertext_blob,
        encryption_algorithm=encryption_algorithm,
        encryption_context=encryption_context,
    )

    response = client.decrypt(request)
    logger.info(
        "Payload decrypted with KMS key %s using %s",
        response.key_id,
        response.encryption_algorithm,
    )
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Decrypt a payload using AWS KMS")
    parser.add_argument(
        "--ciphertext",
        help="Base64-encoded ciphertext blob to decrypt",
    )
    parser.add_argument(
        "--ciphertext-file",
        help="Path to file containing base64-encoded ciphertext",
    )
    parser.add_argument("--key-id", help="KMS key ID or ARN or alias")
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
    parser.add_argument(
        "--output-file",
        help="Path to write decrypted plaintext",
    )
    args = parser.parse_args()

    if args.ciphertext_file:
        with open(args.ciphertext_file, "r") as f:
            b64_ciphertext = f.read().strip()
    elif args.ciphertext:
        b64_ciphertext = args.ciphertext
    else:
        print("Error: provide --ciphertext or --ciphertext-file", file=sys.stderr)
        sys.exit(1)

    ciphertext_blob = decode_base64_to_bytes(b64_ciphertext)
    algorithm = EncryptionAlgorithm(args.algorithm)

    encryption_context = None
    if args.context_key:
        ctx = {}
        for kv in args.context_key:
            k, v = kv.split("=", 1)
            ctx[k] = v
        encryption_context = ctx

    response = decrypt_payload(
        ciphertext_blob=ciphertext_blob,
        key_id=args.key_id,
        encryption_algorithm=algorithm,
        encryption_context=encryption_context,
        region_name=args.region,
    )

    plaintext_str = response.plaintext.decode("utf-8", errors="replace")

    if args.output_file:
        with open(args.output_file, "wb") as f:
            f.write(response.plaintext)
        print(f"Decrypted plaintext written to {args.output_file}")
    else:
        print(f"KeyId: {response.key_id}")
        print(f"EncryptionAlgorithm: {response.encryption_algorithm}")
        print(f"Plaintext: {plaintext_str}")


if __name__ == "__main__":
    main()
