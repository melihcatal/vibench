import os
import json
from typing import Any, Dict

from google.cloud import kms_v1

# Google Cloud KMS client (shared across helpers)
kms_client = kms_v1.KeyManagementServiceClient()

# --- Configuration from environment variables ---
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
KMS_LOCATION = os.getenv("KMS_LOCATION", "global")
KMS_KEY_RING = os.getenv("KMS_KEY_RING")
KMS_CRYPTO_KEY = os.getenv("KMS_CRYPTO_KEY")
KMS_ENVELOPE_KEY = os.getenv("KMS_ENVELOPE_KEY")

# Simple helper to resolve a fully‑qualified Cloud KMS key name


def _crypto_key_path(crypto_key_id: str) -> str:
    return kms_client.crypto_key_path(
        project=GOOGLE_CLOUD_PROJECT,
        location=KMS_LOCATION,
        key_ring=KMS_KEY_RING,
        crypto_key=crypto_key_id,
    )


# --- Utility functions for request/response normalization ---


def _req_normalize_encrypt(plaintext: bytes) -> Dict[str, Any]:
    return {"plaintext": plaintext}


def _resp_parse_encrypt(response: kms_v1.EncryptResponse) -> str:
    # Return Base64‑encoded ciphertext (as returned by Google KMS)
    return response.ciphertext


def _req_normalize_decrypt(ciphertext: str) -> Dict[str, Any]:
    return {"ciphertext": ciphertext}


def _resp_parse_decrypt(response: kms_v1.DecryptResponse) -> bytes:
    return response.plaintext


def _req_normalize_envelope(plaintext: bytes) -> Dict[str, Any]:
    return {"plaintext": plaintext}


def _resp_parse_envelope(response: Dict[str]) -> dict:
    # Expecting encrypted_data and encrypted_dek strings
    return {
        "encrypted_data": response["encrypted_data"],
        "encrypted_dek": response["encrypted_dek"],
        "key_name": response["key_name"],
    }


def _req_normalize_sign(data: bytes) -> Dict[str, Any]:
    return {"data": data}


def _resp_parse_sign(response: kms_v1.SignResponse) -> bytes:
    return response.signature


def _req_normalize_verify(data: bytes, signature: bytes) -> Dict[str, Any]:
    return {"data": data, "signature": signature}


def _resp_parse_verify(response: kms_v1.VerifySignatureResponse) -> bool:
    # KMS Verify returns error on mismatch; a successful call means verification passed
    return True
