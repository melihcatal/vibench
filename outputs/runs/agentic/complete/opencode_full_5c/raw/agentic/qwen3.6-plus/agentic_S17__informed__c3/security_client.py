import os
import json
import base64
import logging
from typing import Optional, Dict, Any, List
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
    GenerateDataKeyRequest,
    GenerateDataKeyResponse,
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    KeyUsageEvent,
)

logger = logging.getLogger(__name__)

AWS_KMS_ENDPOINT = "https://kms.{region}.amazonaws.com"
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


class KMSConfig:
    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.region = region or DEFAULT_REGION
        self.endpoint_url = endpoint_url or AWS_KMS_ENDPOINT.format(region=self.region)
        self.max_retries = max_retries
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "KMSConfig":
        return cls(
            region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
            endpoint_url=os.environ.get("AWS_KMS_ENDPOINT_URL"),
            max_retries=int(os.environ.get("AWS_KMS_MAX_RETRIES", "3")),
            timeout=int(os.environ.get("AWS_KMS_TIMEOUT", "30")),
        )


class SecurityClient:
    def __init__(self, config: Optional[KMSConfig] = None):
        self.config = config or KMSConfig.from_env()
        self._client = None
        self._usage_log: List[KeyUsageEvent] = []

    @property
    def client(self):
        if self._client is None:
            session = boto3.Session(
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                region_name=self.config.region,
            )
            botocore_config = Config(
                retries={"max_attempts": self.config.max_retries},
                read_timeout=self.config.timeout,
                connect_timeout=self.config.timeout,
            )
            self._client = session.client(
                "kms",
                endpoint_url=self.config.endpoint_url,
                config=botocore_config,
            )
        return self._client

    def _log_event(self, event: KeyUsageEvent):
        self._usage_log.append(event)

    def get_usage_log(self) -> List[KeyUsageEvent]:
        return list(self._usage_log)

    def encrypt(self, request: EncryptRequest) -> EncryptResponse:
        try:
            params = request.to_aws_params()
            response = self.client.encrypt(**params)
            result = EncryptResponse.from_aws_response(response)
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Encrypt",
                    timestamp=self._get_timestamp(),
                    success=True,
                    algorithm=request.encryption_algorithm,
                    encryption_context=request.encryption_context,
                )
            )
            return result
        except ClientError as e:
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Encrypt",
                    timestamp=self._get_timestamp(),
                    success=False,
                    algorithm=request.encryption_algorithm,
                    error_message=str(e),
                )
            )
            raise

    def decrypt(self, request: DecryptRequest) -> DecryptResponse:
        try:
            params = request.to_aws_params()
            response = self.client.decrypt(**params)
            result = DecryptResponse.from_aws_response(response)
            self._log_event(
                KeyUsageEvent(
                    key_id=result.key_id,
                    operation="Decrypt",
                    timestamp=self._get_timestamp(),
                    success=True,
                    algorithm=request.encryption_algorithm,
                    encryption_context=request.encryption_context,
                )
            )
            return result
        except ClientError as e:
            self._log_event(
                KeyUsageEvent(
                    key_id="",
                    operation="Decrypt",
                    timestamp=self._get_timestamp(),
                    success=False,
                    algorithm=request.encryption_algorithm,
                    error_message=str(e),
                )
            )
            raise

    def generate_data_key(
        self, request: GenerateDataKeyRequest
    ) -> GenerateDataKeyResponse:
        try:
            params = request.to_aws_params()
            response = self.client.generate_data_key(**params)
            result = GenerateDataKeyResponse.from_aws_response(response)
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="GenerateDataKey",
                    timestamp=self._get_timestamp(),
                    success=True,
                    algorithm=request.key_spec,
                    encryption_context=request.encryption_context,
                )
            )
            return result
        except ClientError as e:
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="GenerateDataKey",
                    timestamp=self._get_timestamp(),
                    success=False,
                    algorithm=request.key_spec,
                    error_message=str(e),
                )
            )
            raise

    def sign(self, request: SignRequest) -> SignResponse:
        try:
            params = request.to_aws_params()
            response = self.client.sign(**params)
            result = SignResponse.from_aws_response(response)
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Sign",
                    timestamp=self._get_timestamp(),
                    success=True,
                    algorithm=request.signing_algorithm,
                )
            )
            return result
        except ClientError as e:
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Sign",
                    timestamp=self._get_timestamp(),
                    success=False,
                    algorithm=request.signing_algorithm,
                    error_message=str(e),
                )
            )
            raise

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        try:
            params = request.to_aws_params()
            response = self.client.verify(**params)
            result = VerifyResponse.from_aws_response(response)
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Verify",
                    timestamp=self._get_timestamp(),
                    success=True,
                    algorithm=request.signing_algorithm,
                )
            )
            return result
        except ClientError as e:
            self._log_event(
                KeyUsageEvent(
                    key_id=request.key_id,
                    operation="Verify",
                    timestamp=self._get_timestamp(),
                    success=False,
                    algorithm=request.signing_algorithm,
                    error_message=str(e),
                )
            )
            raise

    @staticmethod
    def _get_timestamp() -> str:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def aes_gcm_encrypt(plaintext_bytes: bytes, data_key_bytes: bytes) -> tuple:
        iv = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(data_key_bytes),
            modes.GCM(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
        tag = encryptor.tag
        return iv, ciphertext + tag

    @staticmethod
    def aes_gcm_decrypt(
        ciphertext_with_tag: bytes, data_key_bytes: bytes, iv: bytes
    ) -> bytes:
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]
        cipher = Cipher(
            algorithms.AES(data_key_bytes),
            modes.GCM(iv, tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext


def load_config_from_file(config_path: str = "kms_config.json") -> KMSConfig:
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        return KMSConfig(
            region=data.get("region", DEFAULT_REGION),
            endpoint_url=data.get("endpoint_url"),
            max_retries=data.get("max_retries", 3),
            timeout=data.get("timeout", 30),
        )
    return KMSConfig.from_env()
