from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_client import build_kms_client, resolve_kms_key_id, resolve_region
from security_models import EncryptRequest, EncryptResponse, normalize_bytes, normalize_text


def encrypt_payload(plaintext: Any, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> EncryptResponse:
    region = resolve_region()
    kms = build_kms_client(region)
    resolved_key_id = resolve_kms_key_id(key_id)
    request = EncryptRequest(plaintext=normalize_text(plaintext), key_id=resolved_key_id, encryption_context=encryption_context or {})
    try:
        response = kms.encrypt(
            KeyId=request.key_id,
            Plaintext=normalize_bytes(request.plaintext),
            EncryptionContext=request.encryption_context or None,
        )
        return EncryptResponse.from_kms_response(response, key_id=request.key_id)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"AWS KMS encryption failed: {exc}") from exc


def main() -> Dict[str, Any]:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    return encrypt_payload(plaintext=plaintext, key_id=key_id).to_dict()
