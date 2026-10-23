"""
Local helper: Provide local configuration and client helper utilities for Key Management and Encryption.
Uses AWS KMS (boto3) as the concrete provider for key management operations.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from security_models import (
    DecryptRequest,
    DecryptResponse,
    EncryptRequest,
    EncryptResponse,
    EnvelopeEncryptResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
)

logger = logging.getLogger(__name__)


class KMSClientHelper:
    """
    Configuration and client helper for AWS KMS key management and encryption.
    Provider signal: boto3 KMS client, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.
    """

    def __init__(
        self,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ):
        self.region_name = region_name or os.environ.get(
            "AWS_DEFAULT_REGION", "us-east-1"
        )
        self.endpoint_url = endpoint_url or os.environ.get("AWS_KMS_ENDPOINT_URL")
        self.aws_access_key_id = aws_access_key_id or os.environ.get(
            "AWS_ACCESS_KEY_ID"
        )
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.aws_session_token = aws_session_token or os.environ.get(
            "AWS_SESSION_TOKEN"
        )

        config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
        )

        client_kwargs: Dict[str, Any] = {
            "service_name": "kms",
            "region_name": self.region_name,
            "config": config,
        }
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url
        if self.aws_access_key_id and self.aws_secret_access_key:
            client_kwargs["aws_access_key_id"] = self.aws_access_key_id
            client_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            if self.aws_session_token:
                client_kwargs["aws_session_token"] = self.aws_session_token

        self.kms_client = boto3.client(**client_kwargs)

    def encrypt(self, request: EncryptRequest) -> EncryptResponse:
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Plaintext": request.plaintext,
        }
        if request.encryption_algorithm:
            params["EncryptionAlgorithm"] = request.encryption_algorithm.value
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context

        response = self.kms_client.encrypt(**params)
        logger.info("KMS encrypt completed for key %s", request.key_id)
        return EncryptResponse(
            ciphertext_blob=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )

    def decrypt(self, request: DecryptRequest) -> DecryptResponse:
        params: Dict[str, Any] = {
            "CiphertextBlob": request.ciphertext_blob,
        }
        if request.key_id:
            params["KeyId"] = request.key_id
        if request.encryption_algorithm:
            params["EncryptionAlgorithm"] = request.encryption_algorithm.value
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context

        response = self.kms_client.decrypt(**params)
        logger.info("KMS decrypt completed for key %s", response.get("KeyId", ""))
        return DecryptResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )

    def generate_data_key(self, key_id: str, key_spec: str = "AES_256") -> Dict[str, bytes]:
        response = self.kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec=key_spec,
        )
        return {
            "ciphertext_blob": response["CiphertextBlob"],
            "plaintext_key": response["Plaintext"],
        }

    def sign(self, request: SignRequest) -> SignResponse:
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Message": request.message,
            "SigningAlgorithm": request.signing_algorithm.value,
        }
        if request.message_type == "DIGEST":
            params["MessageType"] = "DIGEST"

        response = self.kms_client.sign(**params)
        logger.info("KMS sign completed for key %s", request.key_id)
        return SignResponse(
            signature=response["Signature"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Message": request.message,
            "Signature": request.signature,
            "SigningAlgorithm": request.signing_algorithm.value,
        }
        if request.message_type == "DIGEST":
            params["MessageType"] = "DIGEST"

        response = self.kms_client.verify(**params)
        logger.info("KMS verify completed for key %s", request.key_id)
        return VerifyResponse(
            signature_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )

    def get_key_metadata(self, key_id: str) -> Dict[str, Any]:
        response = self.kms_client.describe_key(KeyId=key_id)
        return response.get("KeyMetadata", {})

    def list_keys(self, limit: int = 50) -> List[Dict[str, str]]:
        response = self.kms_client.list_keys(Limit=limit)
        return response.get("Keys", [])

    def get_key_usage_summary(self, key_id: str) -> Dict[str, Any]:
        metadata = self.get_key_metadata(key_id)
        return {
            "key_id": metadata.get("KeyId", key_id),
            "key_state": metadata.get("KeyState", "UNKNOWN"),
            "key_usage": metadata.get("KeyUsage", "UNKNOWN"),
            "origin": metadata.get("Origin", "UNKNOWN"),
            "creation_date": metadata.get("CreationDate"),
        }


def create_kms_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> KMSClientHelper:
    return KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
