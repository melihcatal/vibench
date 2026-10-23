# security_models.py
import os
from typing import Any, Dict

# Helper utilities for request/response normalization and validation


class SecurityModels:
    """Local helpers to normalize payloads and extract data from AWS KMS service calls."""

    @staticmethod
    def normalize_encrypt_request(key_id: str, plaintext: bytes) -> Dict[str, Any]:
        return {"key_id": key_id, "plaintext": plaintext}

    @staticmethod
    def normalize_decrypt_request(ciphertext_blob: bytes) -> Dict[str, Any]:
        return {"ciphertext_blob": ciphertext_blob}

    @staticmethod
    def normalize_sign_request(
        key_id: str,
        message: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> Dict[str, Any]:
        return {
            "key_id": key_id,
            "message": message,
            "signing_algorithm": signing_algorithm,
        }

    @staticmethod
    def normalize_verify_request(
        key_id: str,
        message: bytes,
        signature: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> Dict[str, Any]:
        return {
            "key_id": key_id,
            "message": message,
            "signature": signature,
            "signing_algorithm": signing_algorithm,
        }

    @staticmethod
    def extract_encrypt_response(resp: Dict[str, Any]) -> bytes:
        return resp["CiphertextBlob"]

    @staticmethod
    def extract_decrypt_response(resp: Dict[str, Any]) -> bytes:
        return resp["Plaintext"]

    @staticmethod
    def extract_sign_response(resp: Dict[str, Any]) -> bytes:
        return resp["Signature"]

    @staticmethod
    def extract_verify_response(resp: Dict[str, Any]) -> str:
        return resp["SigningResult"]

    @staticmethod
    def is_ciphertext(blob: bytes) -> bool:
        """Simple heuristic: AWS encrypt returns varint of total bytes; if first 4 bytes > 0, treat as ciphertext."""
        if len(blob) < 4:
            return False
        first_four = int.from_bytes(blob[:4], byteorder="big")
        return first_four > 0

    @staticmethod
    def is_plaintext(text: bytes) -> bool:
        """Heuristic: plaintext contains printable ASCII more than 50% of bytes."""
        printable = sum(b >= 32 and b < 127 for b in text)
        return printable / len(text) > 0.5

    @staticmethod
    def is_signature(sig: bytes) -> bool:
        """Cryptographic signatures often have structure (e.g., PKCS#1 padding)."""
        # Rough heuristic: length multiple of 8 and not printable ASCII
        if len(sig) % 8 != 0:
            return False
        printable = sum(b >= 32 and b < 127 for b in sig)
        return printable / len(sig) < 0.1
