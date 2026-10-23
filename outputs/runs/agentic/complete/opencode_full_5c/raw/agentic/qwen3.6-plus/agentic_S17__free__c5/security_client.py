import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone

import boto3
from botocore.config import Config

from security_models import (
    EncryptRequest,
    DecryptRequest,
    GenerateDataKeyRequest,
    SignRequest,
    VerifyRequest,
    EncryptResponse,
    DecryptResponse,
    GenerateDataKeyResponse,
    SignResponse,
    VerifyResponse,
    KeyUsageEvent,
    KeyUsageSummary,
    normalize_payload_to_bytes,
    encode_ciphertext_blob,
    decode_ciphertext_blob,
)

logger = logging.getLogger(__name__)

AWS_KMS_ENDPOINT_URL = os.environ.get(
    "AWS_KMS_ENDPOINT_URL", "https://kms.amazonaws.com"
)
AWS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "")
DEFAULT_KEY_ID = os.environ.get("DEFAULT_KMS_KEY_ID", "")
DEFAULT_SIGNING_KEY_ID = os.environ.get("DEFAULT_KMS_SIGNING_KEY_ID", "")
DEFAULT_ENCRYPTION_CONTEXT = json.loads(
    os.environ.get("DEFAULT_ENCRYPTION_CONTEXT", "{}")
)


class KMSClientConfig:
    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        max_retries: int = 3,
        read_timeout: int = 30,
        connect_timeout: int = 10,
    ):
        self.region = region or AWS_REGION
        self.endpoint_url = endpoint_url or AWS_KMS_ENDPOINT_URL
        self.access_key_id = access_key_id or AWS_ACCESS_KEY_ID
        self.secret_access_key = secret_access_key or AWS_SECRET_ACCESS_KEY
        self.session_token = session_token or AWS_SESSION_TOKEN
        self.max_retries = max_retries
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout

    def to_boto3_config(self) -> Config:
        return Config(
            retries={"max_attempts": self.max_retries, "mode": "adaptive"},
            read_timeout=self.read_timeout,
            connect_timeout=self.connect_timeout,
        )

    def get_boto3_session(self):
        session_kwargs = {"region_name": self.region}
        if self.access_key_id and self.secret_access_key:
            session_kwargs["aws_access_key_id"] = self.access_key_id
            session_kwargs["aws_secret_access_key"] = self.secret_access_key
        if self.session_token:
            session_kwargs["aws_session_token"] = self.session_token
        return boto3.Session(**session_kwargs)


class SecurityClient:
    def __init__(self, config: Optional[KMSClientConfig] = None):
        self.config = config or KMSClientConfig()
        self._session = self.config.get_boto3_session()
        self._kms_client = self._session.client(
            "kms",
            endpoint_url=self.config.endpoint_url
            if self.config.endpoint_url != "https://kms.amazonaws.com"
            else None,
            config=self.config.to_boto3_config(),
        )
        self._usage_log: list[KeyUsageEvent] = []

    @property
    def kms_client(self):
        return self._kms_client

    def _log_event(self, event: KeyUsageEvent):
        self._usage_log.append(event)

    def encrypt(self, request: EncryptRequest) -> EncryptResponse:
        plaintext_bytes = normalize_payload_to_bytes(request.plaintext)
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Plaintext": plaintext_bytes,
        }
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            params["GrantTokens"] = request.grant_tokens
        if request.encryption_algorithm != "SYMMETRIC_DEFAULT":
            params["EncryptionAlgorithm"] = request.encryption_algorithm.value

        try:
            response = self._kms_client.encrypt(**params)
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="encrypt",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=True,
            )
            self._log_event(event)
            return EncryptResponse(
                ciphertext_blob=response["CiphertextBlob"],
                key_id=response["KeyId"],
                encryption_algorithm=response.get(
                    "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
                ),
                request_id=response["ResponseMetadata"]["RequestId"],
                http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            )
        except Exception as exc:
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="encrypt",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=False,
                error_message=str(exc),
            )
            self._log_event(event)
            raise

    def decrypt(self, request: DecryptRequest) -> DecryptResponse:
        params: Dict[str, Any] = {
            "CiphertextBlob": request.ciphertext_blob,
        }
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            params["GrantTokens"] = request.grant_tokens
        if request.key_id:
            params["KeyId"] = request.key_id

        try:
            response = self._kms_client.decrypt(**params)
            event = KeyUsageEvent(
                key_id=response["KeyId"],
                operation="decrypt",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=True,
            )
            self._log_event(event)
            return DecryptResponse(
                plaintext=response["Plaintext"],
                key_id=response["KeyId"],
                encryption_algorithm=response.get(
                    "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
                ),
                request_id=response["ResponseMetadata"]["RequestId"],
                http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            )
        except Exception as exc:
            key_id = request.key_id or "unknown"
            event = KeyUsageEvent(
                key_id=key_id,
                operation="decrypt",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=False,
                error_message=str(exc),
            )
            self._log_event(event)
            raise

    def generate_data_key(
        self, request: GenerateDataKeyRequest
    ) -> GenerateDataKeyResponse:
        params: Dict[str, Any] = {"KeyId": request.key_id}
        if request.key_spec:
            params["KeySpec"] = request.key_spec
        if request.number_of_bytes:
            params["NumberOfBytes"] = request.number_of_bytes
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            params["GrantTokens"] = request.grant_tokens

        try:
            response = self._kms_client.generate_data_key(**params)
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="generate_data_key",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=True,
            )
            self._log_event(event)
            return GenerateDataKeyResponse(
                plaintext_key=response["Plaintext"],
                encrypted_key=response["CiphertextBlob"],
                key_id=response["KeyId"],
                request_id=response["ResponseMetadata"]["RequestId"],
                http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            )
        except Exception as exc:
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="generate_data_key",
                timestamp=datetime.now(timezone.utc).isoformat(),
                encryption_context=request.encryption_context,
                success=False,
                error_message=str(exc),
            )
            self._log_event(event)
            raise

    def sign(self, request: SignRequest) -> SignResponse:
        message_bytes = normalize_payload_to_bytes(request.message)
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Message": message_bytes,
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }

        try:
            response = self._kms_client.sign(**params)
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="sign",
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=True,
            )
            self._log_event(event)
            return SignResponse(
                signature=response["Signature"],
                key_id=response["KeyId"],
                signing_algorithm=response["SigningAlgorithm"],
                request_id=response["ResponseMetadata"]["RequestId"],
                http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            )
        except Exception as exc:
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="sign",
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=False,
                error_message=str(exc),
            )
            self._log_event(event)
            raise

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        message_bytes = normalize_payload_to_bytes(request.message)
        params: Dict[str, Any] = {
            "KeyId": request.key_id,
            "Message": message_bytes,
            "Signature": request.signature,
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }

        try:
            response = self._kms_client.verify(**params)
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="verify",
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=response["SignatureValid"],
            )
            self._log_event(event)
            return VerifyResponse(
                signature_valid=response["SignatureValid"],
                key_id=response["KeyId"],
                signing_algorithm=response["SigningAlgorithm"],
                request_id=response["ResponseMetadata"]["RequestId"],
                http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            )
        except Exception as exc:
            event = KeyUsageEvent(
                key_id=request.key_id,
                operation="verify",
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=False,
                error_message=str(exc),
            )
            self._log_event(event)
            raise

    def get_usage_log(self) -> list[KeyUsageEvent]:
        return list(self._usage_log)

    def get_usage_summary(self, key_id: Optional[str] = None) -> KeyUsageSummary:
        events = self._usage_log
        if key_id:
            events = [e for e in events if e.key_id == key_id]

        summary = KeyUsageSummary(key_id=key_id or "all")
        summary.events = events
        summary.total_operations = len(events)
        for event in events:
            if not event.success:
                summary.failed_operations += 1
            if event.operation == "encrypt":
                summary.encrypt_count += 1
            elif event.operation == "decrypt":
                summary.decrypt_count += 1
            elif event.operation == "sign":
                summary.sign_count += 1
            elif event.operation == "verify":
                summary.verify_count += 1
            elif event.operation == "generate_data_key":
                summary.generate_data_key_count += 1
        return summary


def create_security_client(config: Optional[KMSClientConfig] = None) -> SecurityClient:
    return SecurityClient(config=config)
