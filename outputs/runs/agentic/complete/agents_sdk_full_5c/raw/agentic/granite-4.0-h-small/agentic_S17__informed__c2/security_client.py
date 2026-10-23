import os
import base64
from google.cloud import kms_v1
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from typing import Any, Dict

class KmsClient:
    """Local helper to create and reuse a Google Cloud KMS client with service‑account credentials.
    The client is instantiated using GOOGLE_APPLICATION_CREDENTIALS environment variable or explicit JSON blob.
    All public methods forward calls to the underlying kms_v1.KeyManagementServiceClient.
    """
    _client: kms_v1.KeyManagementServiceClient | None = None
    _project_id: str | None = None

    def __init__(self):
        self._init_client()

    def _init_client(self) -> None:
        # Determine credentials path or raw JSON from env
        credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials:
            raise EnvironmentError('Set GOOGLE_APPLICATION_CREDENTIALS to a service‑account JSON file path')
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(credentials)
        # Create client with explicit project ID (required for KMS)
        self._project_id = os.getenv('GCP_PROJECT') or creds.project_id or 'your-project-id'
        self._client = kms_v1.KeyManagementServiceClient(credentials=creds)

    def encrypt(self, crypto_key_path: str, plaintext: bytes) -> kms_v1.types.EncryptResponse:
        """Call the KMS Encrypt API.
        Args:
            crypto_key_path (str): Full resource name (e.g., projects/.../locations/.../keyRings/.../cryptoKeys/...).
            plaintext (bytes): Data to encrypt.
        Returns:
            EncryptResponse object from the SDK.
        """
        request = kms_v1.types.EncryptRequest(name=crypto_key_path, plaintext=plaintext)
        return self._client.encrypt(request=request)

    def decrypt(self, crypto_key_path: str, ciphertext: bytes) -> kms_v1.types.DecryptResponse:
        """
        Args:
            crypto_key_path (str): Full KMS resource name.
            ciphertext (bytes): Encrypted data.
        Returns:
            DecryptResponse object.
        """
        request = kms_v1.types.DecryptRequest(name=crypto_key_path, ciphertext=ciphertext)
        return self._client.decrypt(request=request)

    def asymmetric_sign(self, crypto_key_path: str, message: bytes) -> kms_v1.types.AsymmetricSignResponse:
        """
        Args:
            crypto_key_path (str): Full resource name of an asymmetric key with SIGNATURE usage.
            message (bytes): Message bytes to sign.
        Returns:
            AsymmetricSignResponse object.
        """
        request = kms_v1.types.AsymmetricSignRequest(name=crypto_key_path, message=message)
        return self._client.asymmetric_sign(request=request)

    def asymmetric_verify(self, crypto_key_path: str, message: bytes, signature: bytes) -> bool:
        """
        Args:
            crypto_key_path (str): Full resource name of the asymmetric verification key.
            message (bytes): Signed message.
            signature (bytes): Signature bytes.
        Returns:
            bool: True if verification succeeds, raises otherwise.
        """
        request = kms_v1.types.AsymmetricVerifyRequest(name=crypto_key_path, message=message, signature=signature)
        self._client.asymmetric_verify(request=request)
        return True
