"""
[SAME-SCENARIO] envelope_encrypt.py - Implements envelope encryption using a managed key service.

Envelope encryption workflow:
1. Generate a data key using AWS KMS managed key
2. Encrypt the plaintext locally with the data key (AES-GCM)
3. Store the encrypted data key alongside the ciphertext

Provider: AWS Key Management Service (AWS KMS)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import argparse
import logging
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Optional

from security_client import KMSClientHelper
from security_models import (
    EnvelopeEncryptResponse,
    build_encryption_context,
    encode_bytes_to_base64,
    decode_base64_to_bytes,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")


def envelope_encrypt(
    key_id: str,
    plaintext: bytes,
    key_spec: str = "AES_256",
    encryption_context: Optional[dict] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> EnvelopeEncryptResponse:
    """
    Perform envelope encryption using AWS KMS to wrap a locally generated data key.

    Steps:
    1. Call KMS GenerateDataKey to get an encrypted+plaintext data key pair
    2. Use the plaintext data key to encrypt the payload locally with AES-GCM
    3. Return the encrypted data key, IV, ciphertext, and metadata

    Provider: AWS KMS (boto3) via security_client.KMSClientHelper
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    logger.info("Generating data key via KMS for key_id=%s", key_id)
    data_key_response = client.generate_data_key(key_id=key_id, key_spec=key_spec)
    plaintext_data_key = data_key_response["plaintext_key"]
    encrypted_data_key = data_key_response["ciphertext_blob"]

    aesgcm = AESGCM(plaintext_data_key)
    iv = os.urandom(12)

    enc_context = encryption_context or {}
    associated_data = _serialize_context_for_aad(enc_context)

    ciphertext = aesgcm.encrypt(iv, plaintext, associated_data)

    response = EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key,
        plaintext_data_key=plaintext_data_key,
        ciphertext=ciphertext,
        key_id=key_id,
        iv=iv,
        algorithm=f"KMS_{key_spec}/AES_GCM",
    )

    logger.info(
        "Envelope encryption completed: key_id=%s, algorithm=%s, iv_len=%d",
        response.key_id,
        response.algorithm,
        len(response.iv),
    )
    return response


def envelope_decrypt(
    encrypted_data_key: bytes,
    ciphertext: bytes,
    iv: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[dict] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> bytes:
    """
    Decrypt an envelope-encrypted payload using AWS KMS to unwrap the data key.

    Provider: AWS KMS (boto3) via security_client.KMSClientHelper
    """
    from security_models import DecryptRequest, EncryptionAlgorithm

    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    decrypt_request = DecryptRequest(
        key_id=key_id,
        ciphertext_blob=encrypted_data_key,
        encryption_algorithm=EncryptionAlgorithm.SYMMETRIC_DEFAULT,
        encryption_context=encryption_context,
    )

    decrypt_response = client.decrypt(decrypt_request)
    plaintext_data_key = decrypt_response.plaintext

    aesgcm = AESGCM(plaintext_data_key)
    associated_data = _serialize_context_for_aad(encryption_context or {})

    plaintext = aesgcm.decrypt(iv, ciphertext, associated_data)
    logger.info("Envelope decryption completed successfully")
    return plaintext


def _serialize_context_for_aad(encryption_context: dict) -> bytes:
    if not encryption_context:
        return b""
    sorted_items = sorted(encryption_context.items())
    aad_str = "&".join(f"{k}={v}" for k, v in sorted_items)
    return aad_str.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Envelope encrypt a payload using AWS KMS"
    )
    parser.add_argument(
        "action",
        choices=["encrypt", "decrypt"],
        help="Action to perform",
    )
    parser.add_argument("--key-id", help="KMS key ID or ARN or alias")
    parser.add_argument(
        "--plaintext",
        help="Plaintext string to encrypt (encrypt action)",
    )
    parser.add_argument(
        "--plaintext-file",
        help="Path to file with plaintext (encrypt action)",
    )
    parser.add_argument(
        "--encrypted-data-key",
        help="Base64-encoded encrypted data key (decrypt action)",
    )
    parser.add_argument(
        "--encrypted-data-key-file",
        help="Path to file with encrypted data key (decrypt action)",
    )
    parser.add_argument(
        "--ciphertext",
        help="Base64-encoded ciphertext (decrypt action)",
    )
    parser.add_argument(
        "--ciphertext-file",
        help="Path to file with ciphertext (decrypt action)",
    )
    parser.add_argument(
        "--iv",
        help="Base64-encoded IV (decrypt action)",
    )
    parser.add_argument("--iv-file", help="Path to file with IV (decrypt action)")
    parser.add_argument("--region", help="AWS region for KMS")
    parser.add_argument(
        "--context-key",
        action="append",
        help="Encryption context key=value pairs",
    )
    args = parser.parse_args()

    encryption_context = None
    if args.context_key:
        ctx = {}
        for kv in args.context_key:
            k, v = kv.split("=", 1)
            ctx[k] = v
        encryption_context = ctx

    if args.action == "encrypt":
        if args.plaintext_file:
            with open(args.plaintext_file, "rb") as f:
                plaintext = f.read()
        elif args.plaintext:
            plaintext = args.plaintext.encode("utf-8")
        else:
            parser.error("--plaintext or --plaintext-file required for encrypt")

        response = envelope_encrypt(
            key_id=args.key_id,
            plaintext=plaintext,
            encryption_context=encryption_context,
            region_name=args.region,
        )

        print(f"KeyId: {response.key_id}")
        print(f"Algorithm: {response.algorithm}")
        print(f"EncryptedDataKey (base64): {encode_bytes_to_base64(response.encrypted_data_key)}")
        print(f"IV (base64): {encode_bytes_to_base64(response.iv)}")
        print(f"Ciphertext (base64): {encode_bytes_to_base64(response.ciphertext)}")

    elif args.action == "decrypt":
        if args.encrypted_data_key_file:
            with open(args.encrypted_data_key_file, "r") as f:
                enc_data_key_b64 = f.read().strip()
        elif args.encrypted_data_key:
            enc_data_key_b64 = args.encrypted_data_key
        else:
            parser.error("--encrypted-data-key or --encrypted-data-key-file required for decrypt")

        if args.ciphertext_file:
            with open(args.ciphertext_file, "r") as f:
                ciphertext_b64 = f.read().strip()
        elif args.ciphertext:
            ciphertext_b64 = args.ciphertext
        else:
            parser.error("--ciphertext or --ciphertext-file required for decrypt")

        if args.iv_file:
            with open(args.iv_file, "r") as f:
                iv_b64 = f.read().strip()
        elif args.iv:
            iv_b64 = args.iv
        else:
            parser.error("--iv or --iv-file required for decrypt")

        encrypted_data_key = decode_base64_to_bytes(enc_data_key_b64)
        ciphertext = decode_base64_to_bytes(ciphertext_b64)
        iv = decode_base64_to_bytes(iv_b64)

        plaintext = envelope_decrypt(
            encrypted_data_key=encrypted_data_key,
            ciphertext=ciphertext,
            iv=iv,
            key_id=args.key_id,
            encryption_context=encryption_context,
            region_name=args.region,
        )
        print(f"Decrypted plaintext: {plaintext.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    main()
