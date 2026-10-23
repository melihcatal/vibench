from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError

from security_models import (
    DecryptionRequest,
    DecryptionResponse,
    EncryptionRequest,
    EncryptionResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)


@dataclass
class KmsConfig:
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None


def load_kms_config() -> KmsConfig:
    return KmsConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("AWS_KMS_ENDPOINT_URL"),
    )


def build_kms_client(config: Optional[KmsConfig] = None) -> BaseClient:
    config = config or load_kms_config()
    return boto3.client(
        "kms",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
    )


def _metadata_from_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v
        for k, v in response.items()
        if k not in {"CiphertextBlob", "Plaintext", "Signature"}
    }


class AwsKmsSecurityClient:
    def __init__(self, client: Optional[BaseClient] = None) -> None:
        self.client = client or build_kms_client()

    def encrypt(self, request: EncryptionRequest) -> EncryptionResponse:
        params: Dict[str, Any] = {"KeyId": request.key_id, "Plaintext": request.plaintext}
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        response = self.client.encrypt(**params)
        return EncryptionResponse(
            key_id=request.key_id,
            ciphertext=response["CiphertextBlob"],
            algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
            metadata=_metadata_from_response(response),
        )

    def decrypt(self, request: DecryptionRequest) -> DecryptionResponse:
        params: Dict[str, Any] = {"CiphertextBlob": request.ciphertext, "KeyId": request.key_id}
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        response = self.client.decrypt(**params)
        return DecryptionResponse(
            key_id=request.key_id,
            plaintext=response["Plaintext"],
            algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
            metadata=_metadata_from_response(response),
        )

    def sign(self, request: SignRequest) -> SignResponse:
        response = self.client.sign(
            KeyId=request.key_id,
            Message=request.message,
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return SignResponse(
            key_id=request.key_id,
            signature=response["Signature"],
            algorithm=response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
            metadata=_metadata_from_response(response),
        )

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        response = self.client.verify(
            KeyId=request.key_id,
            Message=request.message,
            MessageType="RAW",
            Signature=request.signature,
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return VerifyResponse(
            key_id=request.key_id,
            verified=bool(response.get("SignatureValid", False)),
            algorithm=response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
            metadata=_metadata_from_response(response),
        )


def encode_blob(blob: bytes) -> str:
    return base64.b64encode(blob).decode("ascii")


def decode_blob(blob_text: str) -> bytes:
    return base64.b64decode(blob_text.encode("ascii"))


def handle_aws_errors(error: Exception) -> str:
    if isinstance(error, (ClientError, BotoCoreError)):
        return str(error)
    return f"Unexpected security client error: {error}"
