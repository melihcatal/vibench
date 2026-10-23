import base64
import json
from typing import Any, Dict


class SecurityModels:
    """Normalization helpers for request/response payloads for key management."""

    @staticmethod
    def normalize_encrypt_request(
        payload: str, key_identifier: str, algorithm: str = "AES"
    ) -> Dict[str, Any]:
        return {
            "key_id": key_identifier,
            "plaintext": base64.b64encode(payload.encode()).decode(),
            "algorithm": algorithm,
        }

    @staticmethod
    def parse_encrypt_response(response: Dict[str, Any]) -> Dict[str, Any]:
        # Sample AWS KMS response fields (adapt as needed per provider)
        return {
            "ciphertext_blob": base64.b64decode(response.get("CiphertextBlob", "")),
            "key_id": response.get("KeyId"),
        }

    @staticmethod
    def normalize_decrypt_request(
        ciphertext_blob: str, key_identifier: str
    ) -> Dict[str, Any]:
        return {
            "key_id": key_identifier,
            "ciphertext_blob": base64.b64encode(ciphertext_blob.encode()).decode(),
        }

    @staticmethod
    def parse_decrypt_response(response: Dict[str, Any]) -> str:
        plaintext_b64 = response.get("Plaintext")
        return base64.b64decode(plaintext_b64).decode() if plaintext_b64 else ""

    @staticmethod
    def normalize_sign_request(
        data: str, key_identifier: str, digest_algorithm: str = "SHA256"
    ) -> Dict[str, Any]:
        return {
            "key_id": key_identifier,
            "data": base64.b64encode(data.encode()).decode(),
            "digest_algorithm": digest_algorithm,
        }

    @staticmethod
    def parse_sign_response(response: Dict[str, Any]) -> str:
        return base64.b64decode(response.get("Signature", "")).decode()

    @staticmethod
    def normalize_verify_request(
        data: str, signature: str, key_identifier: str, digest_algorithm: str = "SHA256"
    ) -> Dict[str, Any]:
        return {
            "key_id": key_identifier,
            "data": base64.b64encode(data.encode()).decode(),
            "signature": base64.b64encode(signature.encode()).decode(),
            "digest_algorithm": digest_algorithm,
        }

    @staticmethod
    def parse_verify_response(response: Dict[str, Any]) -> bool:
        # Most services return a boolean-like field
        return response.get("SignatureValid", False)
