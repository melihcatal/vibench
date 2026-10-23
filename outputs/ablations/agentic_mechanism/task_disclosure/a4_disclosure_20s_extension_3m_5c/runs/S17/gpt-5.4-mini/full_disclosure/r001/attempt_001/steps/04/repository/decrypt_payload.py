import base64
import json
import os
from typing import Any, Dict, Optional

import boto3


def _load_ciphertext(payload: str) -> bytes:
    try:
        raw = json.loads(payload)
        if isinstance(raw, dict):
            candidate = raw.get("ciphertext") or raw.get("CiphertextBlob") or raw.get("ciphertext_blob")
            if isinstance(candidate, str):
                return base64.b64decode(candidate)
        return base64.b64decode(payload)
    except Exception:
        return payload.encode("utf-8")


def decrypt_payload(ciphertext_payload: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> str:
    kms = boto3.client("kms")
    kwargs: Dict[str, Any] = {"CiphertextBlob": _load_ciphertext(ciphertext_payload)}
    if key_id:
        kwargs["KeyId"] = key_id
    if encryption_context:
        kwargs["EncryptionContext"] = encryption_context
    response = kms.decrypt(**kwargs)
    plaintext = response["Plaintext"]
    if isinstance(plaintext, bytes):
        return plaintext.decode("utf-8")
    return bytes(plaintext).decode("utf-8")


def main() -> None:
    payload = os.environ.get("CIPHERTEXT_PAYLOAD", "")
    key_id = os.environ.get("KMS_KEY_ID")
    encryption_context_raw = os.environ.get("KMS_ENCRYPTION_CONTEXT")
    encryption_context = json.loads(encryption_context_raw) if encryption_context_raw else None
    print(decrypt_payload(payload, key_id=key_id, encryption_context=encryption_context))


if __name__ == "__main__":
    main()
