import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    CryptoAction,
    DecryptionRequest,
    DecryptionResponse,
    EncryptionRequest,
    EncryptionResponse,
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    KeyUsageEvent,
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)

AWS_KMS_ENDPOINT = "https://kms.{region}.amazonaws.com"
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.environ.get("AWS_KMS_KEY_ID", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "")


class KMSClientWrapper:
    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ):
        self.region = region or DEFAULT_REGION
        self.endpoint_url = endpoint_url or AWS_KMS_ENDPOINT.format(region=self.region)
        self.aws_access_key_id = aws_access_key_id or AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = aws_secret_access_key or AWS_SECRET_ACCESS_KEY
        self.aws_session_token = aws_session_token or AWS_SESSION_TOKEN
        self._client = None
        self.usage_log: List[KeyUsageEvent] = []

    @property
    def client(self):
        if self._client is None:
            session_kwargs = {
                "region_name": self.region,
                "aws_access_key_id": self.aws_access_key_id,
                "aws_secret_access_key": self.aws_secret_access_key,
            }
            if self.aws_session_token:
                session_kwargs["aws_session_token"] = self.aws_session_token
            session = boto3.Session(**session_kwargs)
            config = Config(
                retries={"max_attempts": 3, "mode": "adaptive"},
                connect_timeout=5,
                read_timeout=30,
            )
            self._client = session.client(
                "kms",
                endpoint_url=self.endpoint_url,
                config=config,
            )
        return self._client

    def encrypt(self, request: EncryptionRequest) -> EncryptionResponse:
        try:
            payload = request.to_provider_payload()
            response = self.client.encrypt(**payload)
            enc_response = EncryptionResponse.from_provider_response(response)
            self._log_usage(
                request.key_id, CryptoAction.ENCRYPT, enc_response.request_id, True
            )
            return enc_response
        except ClientError as e:
            self._log_usage(request.key_id, CryptoAction.ENCRYPT, "", False, str(e))
            raise

    def decrypt(self, request: DecryptionRequest) -> DecryptionResponse:
        try:
            payload = request.to_provider_payload()
            response = self.client.decrypt(**payload)
            dec_response = DecryptionResponse.from_provider_response(response)
            self._log_usage(
                dec_response.key_id, CryptoAction.DECRYPT, dec_response.request_id, True
            )
            return dec_response
        except ClientError as e:
            self._log_usage("", CryptoAction.DECRYPT, "", False, str(e))
            raise

    def generate_data_key(
        self,
        key_id: str,
        key_spec: str = "AES_256",
        encryption_context: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        try:
            params = {"KeyId": key_id, "KeySpec": key_spec}
            if encryption_context:
                params["EncryptionContext"] = encryption_context
            response = self.client.generate_data_key(**params)
            self._log_usage(
                key_id,
                CryptoAction.ENVELOPE_ENCRYPT,
                response.get("ResponseMetadata", {}).get("RequestId", ""),
                True,
            )
            return response
        except ClientError as e:
            self._log_usage(key_id, CryptoAction.ENVELOPE_ENCRYPT, "", False, str(e))
            raise

    def sign(self, request: SigningRequest) -> SigningResponse:
        try:
            payload = request.to_provider_payload()
            response = self.client.sign(**payload)
            sign_response = SigningResponse.from_provider_response(response)
            self._log_usage(
                request.key_id, CryptoAction.SIGN, sign_response.request_id, True
            )
            return sign_response
        except ClientError as e:
            self._log_usage(request.key_id, CryptoAction.SIGN, "", False, str(e))
            raise

    def verify(self, request: VerificationRequest) -> VerificationResponse:
        try:
            payload = request.to_provider_payload()
            response = self.client.verify(**payload)
            verify_response = VerificationResponse.from_provider_response(response)
            self._log_usage(
                request.key_id, CryptoAction.VERIFY, verify_response.request_id, True
            )
            return verify_response
        except ClientError as e:
            self._log_usage(request.key_id, CryptoAction.VERIFY, "", False, str(e))
            raise

    def get_key_usage_events(self) -> List[KeyUsageEvent]:
        return list(self.usage_log)

    def _log_usage(
        self,
        key_id: str,
        action: CryptoAction,
        request_id: str,
        success: bool,
        error_message: Optional[str] = None,
    ):
        from datetime import datetime, timezone

        event = KeyUsageEvent(
            key_id=key_id,
            action=action,
            timestamp=datetime.now(timezone.utc).isoformat(),
            request_id=request_id,
            success=success,
            error_message=error_message,
        )
        self.usage_log.append(event)

    def describe_key(self, key_id: str) -> Dict[str, Any]:
        try:
            response = self.client.describe_key(KeyId=key_id)
            return response.get("KeyMetadata", {})
        except ClientError as e:
            raise


def create_kms_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> KMSClientWrapper:
    return KMSClientWrapper(
        region=region,
        endpoint_url=endpoint_url,
    )


def load_config_from_env() -> Dict[str, str]:
    return {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "aws_session_token": AWS_SESSION_TOKEN,
        "aws_default_region": DEFAULT_REGION,
        "aws_kms_key_id": AWS_KMS_KEY_ID,
        "aws_kms_endpoint": AWS_KMS_ENDPOINT.format(region=DEFAULT_REGION),
    }
