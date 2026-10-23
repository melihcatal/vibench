import os
import json
import base64
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

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
    KeyMetadata,
    KeyUsageSummary,
    KeyUsageEvent,
    parse_kms_response_metadata,
)

logger = logging.getLogger(__name__)

AWS_KMS_ENDPOINT = "https://kms.{region}.amazonaws.com"
DEFAULT_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)


class KMSConfig:
    def __init__(
        self,
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        kms_key_id: Optional[str] = None,
        signing_key_id: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.region = region or DEFAULT_REGION
        self.aws_access_key_id = aws_access_key_id or os.environ.get(
            "AWS_ACCESS_KEY_ID"
        )
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.aws_session_token = aws_session_token or os.environ.get(
            "AWS_SESSION_TOKEN"
        )
        self.kms_key_id = kms_key_id or os.environ.get("AWS_KMS_KEY_ID")
        self.signing_key_id = signing_key_id or os.environ.get("AWS_KMS_SIGNING_KEY_ID")
        self.max_retries = max_retries
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "KMSConfig":
        return cls(
            region=os.environ.get(
                "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
            ),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
            kms_key_id=os.environ.get("AWS_KMS_KEY_ID"),
            signing_key_id=os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
            max_retries=int(os.environ.get("AWS_MAX_RETRIES", "3")),
            timeout=int(os.environ.get("AWS_TIMEOUT", "30")),
        )

    @classmethod
    def from_file(cls, config_path: str) -> "KMSConfig":
        with open(config_path, "r") as f:
            data = json.load(f)
        return cls(
            region=data.get("region"),
            aws_access_key_id=data.get("aws_access_key_id"),
            aws_secret_access_key=data.get("aws_secret_access_key"),
            aws_session_token=data.get("aws_session_token"),
            kms_key_id=data.get("kms_key_id"),
            signing_key_id=data.get("signing_key_id"),
            max_retries=data.get("max_retries", 3),
            timeout=data.get("timeout", 30),
        )

    def get_boto3_session(self):
        session_kwargs = {}
        if self.aws_access_key_id:
            session_kwargs["aws_access_key_id"] = self.aws_access_key_id
        if self.aws_secret_access_key:
            session_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
        if self.aws_session_token:
            session_kwargs["aws_session_token"] = self.aws_session_token
        if self.region:
            session_kwargs["region_name"] = self.region
        return boto3.Session(**session_kwargs)


class SecurityClient:
    def __init__(self, config: Optional[KMSConfig] = None):
        self.config = config or KMSConfig.from_env()
        self._session = self.config.get_boto3_session()
        self._kms_client = None
        self._cloudtrail_client = None

    @property
    def kms_client(self):
        if self._kms_client is None:
            botocore_config = Config(
                retries={"max_attempts": self.config.max_retries, "mode": "standard"},
                read_timeout=self.config.timeout,
                connect_timeout=self.config.timeout,
            )
            self._kms_client = self._session.client(
                "kms",
                config=botocore_config,
                endpoint_url=AWS_KMS_ENDPOINT.format(region=self.config.region),
            )
        return self._kms_client

    @property
    def cloudtrail_client(self):
        if self._cloudtrail_client is None:
            botocore_config = Config(
                retries={"max_attempts": self.config.max_retries, "mode": "standard"},
                read_timeout=self.config.timeout,
                connect_timeout=self.config.timeout,
            )
            self._cloudtrail_client = self._session.client(
                "cloudtrail",
                config=botocore_config,
            )
        return self._cloudtrail_client

    def encrypt(self, request: EncryptionRequest) -> EncryptionResponse:
        params = {
            "KeyId": request.key_id,
            "Plaintext": request.get_plaintext_bytes(),
            "EncryptionAlgorithm": request.encryption_algorithm.value,
        }
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            params["GrantTokens"] = request.grant_tokens

        response = self.kms_client.encrypt(**params)
        http_metadata = parse_kms_response_metadata(response)

        return EncryptionResponse(
            ciphertext_blob=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_algorithm=response["EncryptionAlgorithm"],
            request_id=http_metadata.get("request_id", ""),
            http_metadata=http_metadata,
        )

    def decrypt(self, request: DecryptionRequest) -> DecryptionResponse:
        params = {
            "CiphertextBlob": request.get_ciphertext_bytes(),
        }
        if request.key_id:
            params["KeyId"] = request.key_id
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context
        if request.encryption_algorithm:
            params["EncryptionAlgorithm"] = request.encryption_algorithm.value
        if request.grant_tokens:
            params["GrantTokens"] = request.grant_tokens

        response = self.kms_client.decrypt(**params)
        http_metadata = parse_kms_response_metadata(response)

        return DecryptionResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=http_metadata.get("request_id", ""),
        )

    def generate_data_key(
        self,
        key_id: str,
        key_spec: str = "AES_256",
        encryption_context: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        params = {
            "KeyId": key_id,
            "KeySpec": key_spec,
        }
        if encryption_context:
            params["EncryptionContext"] = encryption_context

        response = self.kms_client.generate_data_key(**params)
        return {
            "plaintext_key": response["Plaintext"],
            "encrypted_key": response["CiphertextBlob"],
            "key_id": response["KeyId"],
            "key_spec": response.get("KeySpec", key_spec),
        }

    def sign(self, request: SigningRequest) -> SigningResponse:
        params = {
            "KeyId": request.key_id,
            "Message": request.get_message_bytes(),
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context

        response = self.kms_client.sign(**params)
        http_metadata = parse_kms_response_metadata(response)

        return SigningResponse(
            signature=response["Signature"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=http_metadata.get("request_id", ""),
        )

    def verify(self, request: VerificationRequest) -> VerificationResponse:
        params = {
            "KeyId": request.key_id,
            "Message": request.get_message_bytes(),
            "Signature": request.get_signature_bytes(),
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }
        if request.encryption_context:
            params["EncryptionContext"] = request.encryption_context

        response = self.kms_client.verify(**params)
        http_metadata = parse_kms_response_metadata(response)

        return VerificationResponse(
            signature_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=http_metadata.get("request_id", ""),
        )

    def describe_key(self, key_id: str) -> KeyMetadata:
        response = self.kms_client.describe_key(KeyId=key_id)
        key_metadata = response["KeyMetadata"]

        return KeyMetadata(
            key_id=key_metadata["KeyId"],
            key_arn=key_metadata["Arn"],
            key_state=key_metadata["KeyState"],
            key_usage=key_metadata.get("KeyUsage", ""),
            key_spec=key_metadata.get("KeySpec", ""),
            creation_date=key_metadata.get("CreationDate"),
            description=key_metadata.get("Description"),
            enabled=key_metadata.get("Enabled", True),
        )

    def get_key_usage_events(
        self,
        key_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        max_events: int = 100,
    ) -> List[KeyUsageEvent]:
        events = []
        lookup_attributes = [
            {"AttributeKey": "ResourceName", "AttributeValue": key_id},
        ]

        kwargs = {
            "LookupAttributes": lookup_attributes,
            "MaxResults": min(max_events, 50),
        }
        if start_time:
            kwargs["StartTime"] = start_time
        if end_time:
            kwargs["EndTime"] = end_time

        try:
            response = self.cloudtrail_client.lookup_events(**kwargs)
            for event in response.get("Events", []):
                key_usage_event = KeyUsageEvent(
                    event_id=event.get("EventId", ""),
                    key_id=key_id,
                    action=event.get("EventName", ""),
                    timestamp=event.get("EventTime", datetime.utcnow()),
                    principal=event.get("Username"),
                    source_ip=event.get("AccessKeyId"),
                )
                events.append(key_usage_event)
        except ClientError as e:
            logger.warning(f"CloudTrail lookup failed for key {key_id}: {e}")

        return events

    def build_key_usage_summary(
        self,
        key_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> KeyUsageSummary:
        events = self.get_key_usage_events(key_id, start_time, end_time)

        summary = KeyUsageSummary(
            key_id=key_id,
            key_arn="",
            period_start=start_time,
            period_end=end_time,
            events=events,
        )

        try:
            metadata = self.describe_key(key_id)
            summary.key_arn = metadata.key_arn
        except Exception:
            pass

        for event in events:
            action = event.action.upper()
            if "ENCRYPT" in action and "DECRYPT" not in action:
                summary.total_encryptions += 1
            elif "DECRYPT" in action:
                summary.total_decryptions += 1
            elif "SIGN" in action and "VERIFY" not in action:
                summary.total_signatures += 1
            elif "VERIFY" in action:
                summary.total_verifications += 1
            elif "GENERATEDATAKEY" in action:
                summary.total_generate_data_key += 1

        return summary

    def normalize_encryption_context(
        self, context: Optional[Dict[str, str]]
    ) -> Optional[Dict[str, str]]:
        if context is None:
            return None
        return {str(k): str(v) for k, v in context.items()}

    def format_key_arn(
        self,
        key_id: str,
        account_id: Optional[str] = None,
        region: Optional[str] = None,
    ) -> str:
        if key_id.startswith("arn:"):
            return key_id
        actual_region = region or self.config.region
        actual_account = account_id or os.environ.get("AWS_ACCOUNT_ID", "unknown")
        if key_id.startswith("mrk-"):
            return f"arn:aws:kms:{actual_region}:{actual_account}:key/{key_id}"
        return f"arn:aws:kms:{actual_region}:{actual_account}:key/{key_id}"
