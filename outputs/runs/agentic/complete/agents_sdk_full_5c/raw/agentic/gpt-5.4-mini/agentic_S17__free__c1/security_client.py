from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1
from google.cloud import storage

from security_models import CryptoRequest, CryptoResponse


DEFAULT_KMS_KEY_NAME_ENV = "GOOGLE_CLOUD_KMS_KEY_NAME"
DEFAULT_STORAGE_BUCKET_ENV = "GOOGLE_CLOUD_STORAGE_BUCKET"


def load_config() -> Dict[str, Optional[str]]:
    return {
        "kms_key_name": os.getenv(DEFAULT_KMS_KEY_NAME_ENV),
        "storage_bucket": os.getenv(DEFAULT_STORAGE_BUCKET_ENV),
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
    }


def kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def storage_client() -> storage.Client:
    return storage.Client()


def encrypt_with_kms(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    key_name = request.key_id or load_config()["kms_key_name"]
    if not key_name:
        raise ValueError("Missing Google Cloud KMS key name")
    response = client.encrypt(request={"name": key_name, "plaintext": request.payload.encode("utf-8")})
    return CryptoResponse(
        operation="encrypt",
        provider="google_cloud_kms",
        key_id=key_name,
        result={"ciphertext": base64.b64encode(response.ciphertext).decode("utf-8")},
    )


def decrypt_with_kms(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    key_name = request.key_id or load_config()["kms_key_name"]
    if not key_name:
        raise ValueError("Missing Google Cloud KMS key name")
    response = client.decrypt(
        request={"name": key_name, "ciphertext": base64.b64decode(request.payload)}
    )
    return CryptoResponse(
        operation="decrypt",
        provider="google_cloud_kms",
        key_id=key_name,
        result={"plaintext": response.plaintext.decode("utf-8")},
    )


def sign_with_kms(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    key_name = request.key_id or load_config()["kms_key_name"]
    if not key_name:
        raise ValueError("Missing Google Cloud KMS key name")
    response = client.asymmetric_sign(
        request={"name": key_name, "digest": {"sha256": request.payload.encode("utf-8")}}
    )
    return CryptoResponse(
        operation="sign",
        provider="google_cloud_kms",
        key_id=key_name,
        result={"signature": base64.b64encode(response.signature).decode("utf-8")},
    )


def verify_with_kms(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    key_name = request.key_id or load_config()["kms_key_name"]
    if not key_name:
        raise ValueError("Missing Google Cloud KMS key name")
    response = client.asymmetric_verify(
        request={"name": key_name, "digest": {"sha256": request.payload.encode("utf-8")}, "signature": b""}
    )
    return CryptoResponse(
        operation="verify",
        provider="google_cloud_kms",
        key_id=key_name,
        result={"verified": bool(response.verified)},
    )
