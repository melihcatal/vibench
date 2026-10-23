# security_client.py
import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

# AWS KMS (same-scenario)


class SecurityClient:
    """Local configuration and client helper utilities for AWS Key Management Service (KMS)."""

    def __init__(self) -> None:
        self._kms = boto3.client(
            "kms",
            # AWS credentials are picked up from environment variables by botocore
        )

    def encrypt(self, key_id: str, plaintext: bytes) -> Dict[str, Any]:
        """Encrypt a plaintext payload with a managed AWS KMS key."""
        try:
            response = self._kms.encrypt(KeyId=key_id, Plaintext=plaintext)
            return response
        except ClientError as e:
            raise RuntimeError(f"KMS encryption failed: {e}") from e

    def decrypt(self, ciphertext_blob: bytes) -> Dict[str, Any]:
        """Decrypt a ciphertext payload with AWS KMS."""
        try:
            response = self._kms.decrypt(CiphertextBlob=ciphertext_blob)
            return response
        except ClientError as e:
            raise RuntimeError(f"KMS decryption failed: {e}") from e

    def sign(
        self,
        key_id: str,
        message: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> Dict[str, Any]:
        """Sign a message using an asymmetric KMS key."""
        try:
            response = self._kms.sign(
                KeyId=key_id,
                Message=message,
                MessageType="RAW",
                SigningAlgorithm=signing_algorithm,
            )
            return response
        except ClientError as e:
            raise RuntimeError(f"KMS signing failed: {e}") from e

    def verify(
        self,
        key_id: str,
        message: bytes,
        signature: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> Dict[str, Any]:
        """Verify a signature using an asymmetric KMS key."""
        try:
            response = self._kms.verify(
                KeyId=key_id,
                Message=message,
                Signature=signature,
                SigningAlgorithm=signing_algorithm,
                MessageType="RAW",
            )
            return response
        except ClientError as e:
            raise RuntimeError(f"KMS verification failed: {e}") from e


class SecurityModels:
    """Local request, response, and normalization helpers for AWS KMS operations."""

    @staticmethod
    def normalize_encrypt_request(key_id: str, plaintext: bytes) -> Dict[str, Any]:
        return {"key_id": key_id, "plaintext": plaintext}

    @staticmethod
    def normalize_decrypt_request(ciphertext_blob: bytes) -> Dict[str, Any]:
        return {"ciphertext_blob": ciphertext_blob}

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
