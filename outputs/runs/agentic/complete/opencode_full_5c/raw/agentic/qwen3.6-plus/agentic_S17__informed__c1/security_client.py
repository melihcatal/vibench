import os
import base64
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any

from security_models import (
    KMSConfig,
    load_kms_config,
    EncryptionRequest,
    EncryptionResponse,
    DecryptionRequest,
    DecryptionResponse,
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    SignVerifyRequest,
    SignVerifyResponse,
)


class AWSSecurityClient:
    """Client helper for AWS Key Management Service (AWS KMS).

    Provider: AWS Key Management Service
    SDK: boto3
    Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    """

    def __init__(self, config: Optional[KMSConfig] = None):
        self.config = config or load_kms_config()
        self._client = self._create_kms_client()

    def _create_kms_client(self):
        session = boto3.Session(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
            region_name=self.config.region,
        )
        botocore_config = Config(
            retries={"max_attempts": self.config.max_retries},
            read_timeout=self.config.read_timeout,
            connect_timeout=self.config.connect_timeout,
        )
        client_kwargs = {"config": botocore_config}
        if self.config.endpoint_url:
            client_kwargs["endpoint_url"] = self.config.endpoint_url
        return session.client("kms", **client_kwargs)

    @property
    def client(self):
        return self._client

    def encrypt(self, request: EncryptionRequest) -> EncryptionResponse:
        kwargs = {
            "KeyId": request.key_id,
            "Plaintext": request.plaintext,
            "EncryptionAlgorithm": request.algorithm.value,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            kwargs["GrantTokens"] = request.grant_tokens

        response = self._client.encrypt(**kwargs)
        return EncryptionResponse(
            ciphertext_blob=response["CiphertextBlob"],
            key_id=response["KeyId"],
            encryption_algorithm=response["EncryptionAlgorithm"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def decrypt(self, request: DecryptionRequest) -> DecryptionResponse:
        kwargs = {
            "CiphertextBlob": request.ciphertext_blob,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context
        if request.grant_tokens:
            kwargs["GrantTokens"] = request.grant_tokens

        response = self._client.decrypt(**kwargs)
        return DecryptionResponse(
            plaintext=response["Plaintext"],
            key_id=response["KeyId"],
            encryption_algorithm=response["EncryptionAlgorithm"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def generate_data_key(self, request: EnvelopeEncryptionRequest) -> Dict[str, Any]:
        kwargs = {
            "KeyId": request.key_id,
            "NumberOfBytes": request.number_of_bytes,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context

        response = self._client.generate_data_key(**kwargs)
        return {
            "plaintext_data_key": response["Plaintext"],
            "encrypted_data_key": response["CiphertextBlob"],
            "key_id": response["KeyId"],
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
        }

    def sign(self, request: SignVerifyRequest) -> SignVerifyResponse:
        kwargs = {
            "KeyId": request.key_id,
            "Message": request.message,
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context

        response = self._client.sign(**kwargs)
        return SignVerifyResponse(
            signature=response["Signature"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def verify(self, request: SignVerifyRequest) -> SignVerifyResponse:
        kwargs = {
            "KeyId": request.key_id,
            "Message": request.message,
            "Signature": request.signature,
            "SigningAlgorithm": request.signing_algorithm.value,
            "MessageType": request.message_type.value,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context

        response = self._client.verify(**kwargs)
        return SignVerifyResponse(
            signature_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            signing_algorithm=response.get("SigningAlgorithm", ""),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )


def encode_bytes_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def decode_base64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def normalize_plaintext(plaintext: str) -> bytes:
    if isinstance(plaintext, str):
        return plaintext.encode("utf-8")
    return plaintext


def normalize_ciphertext(ciphertext: str) -> bytes:
    return decode_base64_to_bytes(ciphertext)
