"""
Local configuration and client helper utilities for Key Management and Encryption.
Provides AWS KMS client initialization, credential management, and common operations.
"""

import os
import base64
import json
from typing import Optional, Dict, Any, Tuple

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    EncryptionRequest,
    EncryptionResponse,
    DecryptionRequest,
    DecryptionResponse,
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
    normalize_encryption_context,
)


class KMSClientHelper:
    """
    AWS KMS client helper for managing encryption, decryption, signing,
    and key operations. Uses AWS KMS (Amazon Web Services Key Management Service).
    """

    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        profile: Optional[str] = None,
    ):
        """
        Initialize AWS KMS client helper.

        Args:
            region: AWS region (defaults to AWS_DEFAULT_REGION env var).
            endpoint_url: Optional KMS endpoint URL for local testing.
            profile: Optional AWS profile name.
        """
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.endpoint_url = endpoint_url

        session_kwargs = {}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
            region_name=self.region,
        )

        client_kwargs = {"config": config}
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url

        self.kms_client = session.client("kms", **client_kwargs)

    def encrypt(
        self,
        key_id: str,
        plaintext: str,
        encryption_context: Optional[Dict[str, str]] = None,
        algorithm: str = "SYMMETRIC_DEFAULT",
    ) -> EncryptionResponse:
        """
        Encrypt plaintext using AWS KMS managed key.

        Args:
            key_id: KMS key ID or ARN.
            plaintext: Text to encrypt.
            encryption_context: Optional encryption context dict.
            algorithm: Encryption algorithm (default: SYMMETRIC_DEFAULT).

        Returns:
            EncryptionResponse with ciphertext blob.
        """
        try:
            params = {
                "KeyId": key_id,
                "Plaintext": plaintext.encode("utf-8"),
                "EncryptionAlgorithm": algorithm,
            }
            if encryption_context:
                params["EncryptionContext"] = encryption_context

            response = self.kms_client.encrypt(**params)
            return EncryptionResponse(
                ciphertext_blob=response["CiphertextBlob"],
                key_id=response["KeyId"],
                encryption_algorithm=response.get("EncryptionAlgorithm", algorithm),
                response_metadata=response.get("ResponseMetadata", {}),
            )
        except ClientError as e:
            raise KMSError(f"Encryption failed: {e}") from e

    def decrypt(
        self,
        ciphertext_blob: bytes,
        encryption_context: Optional[Dict[str, str]] = None,
    ) -> DecryptionResponse:
        """
        Decrypt ciphertext using AWS KMS.

        Args:
            ciphertext_blob: Encrypted data blob.
            encryption_context: Optional encryption context (must match encryption).

        Returns:
            DecryptionResponse with plaintext.
        """
        try:
            params = {"CiphertextBlob": ciphertext_blob}
            if encryption_context:
                params["EncryptionContext"] = encryption_context

            response = self.kms_client.decrypt(**params)
            return DecryptionResponse(
                plaintext=response["Plaintext"],
                key_id=response["KeyId"],
                response_metadata=response.get("ResponseMetadata", {}),
            )
        except ClientError as e:
            raise KMSError(f"Decryption failed: {e}") from e

    def generate_data_key(
        self, key_id: str, key_spec: str = "AES_256"
    ) -> Tuple[bytes, bytes]:
        """
        Generate a data key encrypted under a KMS key for envelope encryption.

        Args:
            key_id: KMS key ID or ARN.
            key_spec: Key specification (AES_256 or AES_128).

        Returns:
            Tuple of (plaintext_data_key, encrypted_data_key).
        """
        try:
            response = self.kms_client.generate_data_key(
                KeyId=key_id, KeySpec=key_spec
            )
            return response["Plaintext"], response["CiphertextBlob"]
        except ClientError as e:
            raise KMSError(f"Data key generation failed: {e}") from e

    def envelope_encrypt(
        self,
        key_id: str,
        plaintext: str,
        key_spec: str = "AES_256",
    ) -> EnvelopeEncryptionResponse:
        """
        Perform envelope encryption: generate data key, encrypt plaintext locally,
        and return both encrypted data key and ciphertext.

        Args:
            key_id: KMS key ID for wrapping the data key.
            plaintext: Data to encrypt.
            key_spec: Data key specification.

        Returns:
            EnvelopeEncryptionResponse with encrypted keys and ciphertext.
        """
        import cryptography
        from cryptography.fernet import Fernet

        plaintext_data_key, encrypted_data_key = self.generate_data_key(
            key_id, key_spec
        )
        fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
        fernet = Fernet(fernet_key)
        ciphertext = fernet.encrypt(plaintext.encode("utf-8"))

        return EnvelopeEncryptionResponse(
            plaintext_data_key=plaintext_data_key,
            encrypted_data_key=encrypted_data_key,
            ciphertext=ciphertext,
            key_id=key_id,
        )

    def envelope_decrypt(
        self,
        encrypted_data_key: bytes,
        ciphertext: bytes,
    ) -> DecryptionResponse:
        """
        Perform envelope decryption: decrypt data key with KMS, then decrypt payload.

        Args:
            encrypted_data_key: Encrypted data key from KMS.
            ciphertext: Encrypted payload.

        Returns:
            DecryptionResponse with plaintext.
        """
        from cryptography.fernet import Fernet

        response = self.kms_client.decrypt(CiphertextBlob=encrypted_data_key)
        plaintext_data_key = response["Plaintext"]
        key_id = response["KeyId"]

        fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
        fernet = Fernet(fernet_key)
        plaintext = fernet.decrypt(ciphertext)

        return DecryptionResponse(
            plaintext=plaintext,
            key_id=key_id,
        )

    def sign_message(
        self,
        key_id: str,
        message: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> SigningResponse:
        """
        Sign a message using AWS KMS asymmetric key.

        Args:
            key_id: KMS asymmetric key ID.
            message: Message bytes to sign.
            signing_algorithm: Signing algorithm.

        Returns:
            SigningResponse with signature.
        """
        try:
            response = self.kms_client.sign(
                KeyId=key_id,
                Message=message,
                SigningAlgorithm=signing_algorithm,
            )
            return SigningResponse(
                signature=response["Signature"],
                key_id=response["KeyId"],
                signing_algorithm=response["SigningAlgorithm"],
                response_metadata=response.get("ResponseMetadata", {}),
            )
        except ClientError as e:
            raise KMSError(f"Signing failed: {e}") from e

    def verify_signature(
        self,
        key_id: str,
        message: bytes,
        signature: bytes,
        signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
    ) -> VerificationResponse:
        """
        Verify a signature using AWS KMS asymmetric key.

        Args:
            key_id: KMS asymmetric key ID.
            message: Original message bytes.
            signature: Signature to verify.
            signing_algorithm: Signing algorithm used.

        Returns:
            VerificationResponse with validity result.
        """
        try:
            response = self.kms_client.verify(
                KeyId=key_id,
                Message=message,
                Signature=signature,
                SigningAlgorithm=signing_algorithm,
            )
            return VerificationResponse(
                is_valid=response["SignatureValid"],
                key_id=response["KeyId"],
                response_metadata=response.get("ResponseMetadata", {}),
            )
        except ClientError as e:
            raise KMSError(f"Verification failed: {e}") from e

    def describe_key(self, key_id: str) -> Dict[str, Any]:
        """Describe a KMS key."""
        try:
            response = self.kms_client.describe_key(KeyId=key_id)
            return response.get("KeyMetadata", {})
        except ClientError as e:
            raise KMSError(f"Key description failed: {e}") from e

    def list_keys(self, limit: int = 100) -> list:
        """List KMS keys."""
        try:
            response = self.kms_client.list_keys(Limit=limit)
            return response.get("Keys", [])
        except ClientError as e:
            raise KMSError(f"Key listing failed: {e}") from e


class KMSError(Exception):
    """Custom exception for KMS operations."""
    pass


def get_kms_client() -> KMSClientHelper:
    """Factory function to get a configured KMS client helper."""
    return KMSClientHelper()
