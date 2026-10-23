from __future__ import annotations

import base64
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import (
    CiphertextResponse,
    EnvelopeEncryptionResult,
    PayloadRequest,
    SignatureResult,
    normalize_bytes,
    normalize_text,
)

AWS_KMS_REGION_ENV = "AWS_REGION"
AWS_KMS_DEFAULT_KEY_ENV = "AWS_KMS_KEY_ID"
AWS_KMS_CUSTOMER_MASTER_KEY_ENV = "AWS_KMS_CUSTOMER_MASTER_KEY_ID"


class SecurityClientError(RuntimeError):
    pass


class KMSSecurityClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get(AWS_KMS_REGION_ENV)
        self._client = boto3.client("kms", region_name=self.region_name)

    @staticmethod
    def default_key_id() -> Optional[str]:
        return os.environ.get(AWS_KMS_DEFAULT_KEY_ENV) or os.environ.get(AWS_KMS_CUSTOMER_MASTER_KEY_ENV)

    def encrypt(self, request: PayloadRequest) -> CiphertextResponse:
        try:
            params: Dict[str, Any] = {
                "Plaintext": normalize_bytes(request.plaintext),
            }
            if request.key_id or self.default_key_id():
                params["KeyId"] = request.key_id or self.default_key_id()
            if request.context:
                params["EncryptionContext"] = request.context
            response = self._client.encrypt(**params)
            ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("ascii")
            return CiphertextResponse(ciphertext_b64=ciphertext, key_id=response.get("KeyId"), metadata={"provider": "AWS KMS"})
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(f"AWS KMS encrypt failed: {exc}") from exc

    def decrypt(self, ciphertext_b64: str, context: Optional[Dict[str, str]] = None) -> PayloadRequest:
        try:
            params: Dict[str, Any] = {"CiphertextBlob": base64.b64decode(normalize_text(ciphertext_b64))}
            if context:
                params["EncryptionContext"] = context
            response = self._client.decrypt(**params)
            plaintext = normalize_text(response["Plaintext"])
            return PayloadRequest(plaintext=plaintext, key_id=response.get("KeyId"), context=context or {})
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(f"AWS KMS decrypt failed: {exc}") from exc

    def generate_data_key(self, key_id: Optional[str] = None, key_spec: str = "AES_256", context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        try:
            params: Dict[str, Any] = {"KeySpec": key_spec}
            if key_id or self.default_key_id():
                params["KeyId"] = key_id or self.default_key_id()
            if context:
                params["EncryptionContext"] = context
            response = self._client.generate_data_key(**params)
            return {
                "plaintext_data_key_b64": base64.b64encode(response["Plaintext"]).decode("ascii"),
                "encrypted_data_key_b64": base64.b64encode(response["CiphertextBlob"]).decode("ascii"),
                "key_id": response.get("KeyId"),
                "metadata": {"provider": "AWS KMS", "key_spec": key_spec},
            }
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(f"AWS KMS generate_data_key failed: {exc}") from exc

    def sign(self, message: bytes, key_id: Optional[str] = None) -> SignatureResult:
        try:
            params: Dict[str, Any] = {"Message": normalize_bytes(message), "MessageType": "RAW", "SigningAlgorithm": "RSASSA_PSS_SHA_256"}
            if key_id or self.default_key_id():
                params["KeyId"] = key_id or self.default_key_id()
            response = self._client.sign(**params)
            return SignatureResult(signature_b64=base64.b64encode(response["Signature"]).decode("ascii"), key_id=response.get("KeyId"), metadata={"provider": "AWS KMS"})
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(f"AWS KMS sign failed: {exc}") from exc

    def verify(self, message: bytes, signature_b64: str, key_id: Optional[str] = None) -> SignatureResult:
        try:
            params: Dict[str, Any] = {
                "Message": normalize_bytes(message),
                "MessageType": "RAW",
                "Signature": base64.b64decode(normalize_text(signature_b64)),
                "SigningAlgorithm": "RSASSA_PSS_SHA_256",
            }
            if key_id or self.default_key_id():
                params["KeyId"] = key_id or self.default_key_id()
            response = self._client.verify(**params)
            return SignatureResult(signature_b64=signature_b64, verified=bool(response.get("SignatureValid")), key_id=response.get("KeyId"), metadata={"provider": "AWS KMS"})
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(f"AWS KMS verify failed: {exc}") from exc
