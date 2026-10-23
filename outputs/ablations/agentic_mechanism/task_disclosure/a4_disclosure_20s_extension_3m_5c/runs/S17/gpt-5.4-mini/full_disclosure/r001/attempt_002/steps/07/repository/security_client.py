import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3

AWS_KMS_API_VERSION = "2014-11-01"


@dataclass(frozen=True)
class SecurityClientConfig:
    region_name: Optional[str] = None
    kms_key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


def _env_mapping() -> Dict[str, Optional[str]]:
    return {
        "region_name": os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "kms_key_id": os.environ.get("AWS_KMS_KEY_ID"),
    }


def load_security_client_config(**overrides: Any) -> SecurityClientConfig:
    values = _env_mapping()
    values.update({k: v for k, v in overrides.items() if k in values and v is not None})
    encryption_context = overrides.get("encryption_context")
    if encryption_context is not None:
        values["encryption_context"] = encryption_context
    return SecurityClientConfig(
        region_name=values.get("region_name"),
        kms_key_id=values.get("kms_key_id"),
        encryption_context=values.get("encryption_context"),
    )


def create_kms_client(region_name: Optional[str] = None) -> Any:
    resolved_region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return boto3.client("kms", region_name=resolved_region, api_version=AWS_KMS_API_VERSION)


def get_kms_key_id(config: Optional[SecurityClientConfig] = None) -> str:
    resolved = config or load_security_client_config()
    if not resolved.kms_key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return resolved.kms_key_id


def get_encryption_context(config: Optional[SecurityClientConfig] = None) -> Dict[str, str]:
    resolved = config or load_security_client_config()
    return dict(resolved.encryption_context or {})


def build_kms_encrypt_params(plaintext: bytes, config: Optional[SecurityClientConfig] = None) -> Dict[str, Any]:
    resolved = config or load_security_client_config()
    params: Dict[str, Any] = {"Plaintext": plaintext}
    if resolved.kms_key_id:
        params["KeyId"] = resolved.kms_key_id
    if resolved.encryption_context:
        params["EncryptionContext"] = dict(resolved.encryption_context)
    return params


def build_kms_decrypt_params(ciphertext_blob: bytes, config: Optional[SecurityClientConfig] = None) -> Dict[str, Any]:
    resolved = config or load_security_client_config()
    params: Dict[str, Any] = {"CiphertextBlob": ciphertext_blob}
    if resolved.encryption_context:
        params["EncryptionContext"] = dict(resolved.encryption_context)
    return params
