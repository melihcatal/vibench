import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Optional

import requests


GOOGLE_KMS_SIGN_URL_TEMPLATE = "https://cloudkms.googleapis.com/v1/{name}:asymmetricSign"
GOOGLE_KMS_VERIFY_URL_TEMPLATE = "https://cloudkms.googleapis.com/v1/{name}:asymmetricVerify"


@dataclass
class SignOrVerifyResult:
    success: bool
    signature: Optional[str] = None
    verified: Optional[bool] = None
    key_name: Optional[str] = None
    provider: str = "google-cloud-kms"


def _access_token() -> str:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_CLOUD_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing GOOGLE_OAUTH_ACCESS_TOKEN or GOOGLE_CLOUD_ACCESS_TOKEN")
    return token


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {_access_token()}",
        "Content-Type": "application/json",
    }


def _sha256_digest_b64(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


def sign_with_google_kms(key_name: str, message: bytes) -> SignOrVerifyResult:
    payload = {"digest": {"sha256": _sha256_digest_b64(message)}}
    response = requests.post(GOOGLE_KMS_SIGN_URL_TEMPLATE.format(name=key_name), headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    signature = response.json().get("signature")
    return SignOrVerifyResult(success=True, signature=signature, key_name=key_name)


def verify_with_google_kms(key_name: str, message: bytes, signature_b64: str) -> SignOrVerifyResult:
    payload = {"digest": {"sha256": _sha256_digest_b64(message)}, "signature": signature_b64}
    response = requests.post(GOOGLE_KMS_VERIFY_URL_TEMPLATE.format(name=key_name), headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    verified = response.json().get("signatureVerified")
    return SignOrVerifyResult(success=bool(verified), verified=bool(verified), key_name=key_name)


def sign_or_verify_key(action: str, key_name: str, message: bytes, signature_b64: Optional[str] = None) -> SignOrVerifyResult:
    normalized = action.strip().lower()
    if normalized == "sign":
        return sign_with_google_kms(key_name, message)
    if normalized == "verify":
        if signature_b64 is None:
            raise ValueError("signature_b64 is required for verify")
        return verify_with_google_kms(key_name, message, signature_b64)
    raise ValueError("action must be 'sign' or 'verify'")
