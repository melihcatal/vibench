import os

import boto3

from security_client import aws_region, encryption_context, kms_key_id
from security_models import b64d, b64e, normalize_context


def envelope_encrypt(plaintext: bytes, key_id: str = ""):
    kms = boto3.client("kms", region_name=aws_region())
    resolved_key_id = key_id or kms_key_id()
    data_key = kms.generate_data_key(KeyId=resolved_key_id, KeySpec="AES_256", EncryptionContext=normalize_context(encryption_context()))
    plaintext_key = data_key["Plaintext"]
    encrypted_key = data_key["CiphertextBlob"]
    encrypted = bytes(a ^ b for a, b in zip(plaintext, (plaintext_key * ((len(plaintext) // len(plaintext_key)) + 1))[: len(plaintext)]))
    return {"encrypted_data_key": b64e(encrypted_key), "ciphertext": b64e(encrypted), "encryption_context": normalize_context(encryption_context())}


def envelope_decrypt(payload: dict, key_id: str = "") -> bytes:
    kms = boto3.client("kms", region_name=aws_region())
    decrypted_key = kms.decrypt(CiphertextBlob=b64d(payload["encrypted_data_key"]), EncryptionContext=payload.get("encryption_context") or {})["Plaintext"]
    ciphertext = b64d(payload["ciphertext"])
    return bytes(a ^ b for a, b in zip(ciphertext, (decrypted_key * ((len(ciphertext) // len(decrypted_key)) + 1))[: len(ciphertext)]))
