from __future__ import annotations

import os
from typing import Any, Dict, Optional

from botocore.exceptions import BotoCoreError, ClientError

from security_client import build_kms_client, resolve_kms_key_id, resolve_region
from security_models import DecryptRequest, DecryptResponse, normalize_ciphertext_blob


def decrypt_payload(ciphertext_blob: Any, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> DecryptResponse:
    region = resolve_region()
    kms = build_kms_client(region)
    resolved_key_id = resolve_kms_key_id(key_id)
    request = DecryptRequest(ciphertext_blob=normalize_ciphertext_blob(ciphertext_blob), key_id=resolved_key_id, encryption_context=encryption_context or {})
    try:
        kwargs: Dict[str, Any] = {"CiphertextBlob": request.ciphertext_blob}
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context
        if request.key_id:
            kwargs["KeyId"] = request.key_id
        response = kms.decrypt(**kwargs)
        return DecryptResponse.from_kms_response(response)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"AWS KMS decryption failed: {exc}") from exc


def main() -> Dict[str, Any]:
    ciphertext = os.environ.get("CIPHERTEXT_B64", "")
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    return decrypt_payload(ciphertext_blob=ciphertext, key_id=key_id).to_dict()
