from __future__ import annotations

import hashlib
from typing import Optional

from security_client import get_kms_client, kms_key_name
from security_models import SignatureRequest, VerificationRequest, b64decode_str, b64encode_str


_SUPPORTED = {
    "EC_SIGN_P256_SHA256": "sha256",
    "RSA_SIGN_PSS_2048_SHA256": "sha256",
    "RSA_SIGN_PSS_3072_SHA256": "sha256",
    "RSA_SIGN_PSS_4096_SHA256": "sha256",
    "RSA_SIGN_PKCS1_2048_SHA256": "sha256",
    "RSA_SIGN_PKCS1_3072_SHA256": "sha256",
    "RSA_SIGN_PKCS1_4096_SHA256": "sha256",
}


def _digest(message: str, algorithm: str) -> bytes:
    algo_name = _SUPPORTED.get(algorithm, "sha256")
    return getattr(hashlib, algo_name)(message.encode("utf-8")).digest()


def sign_message(message: str, key_version_name: Optional[str] = None, algorithm: str = "RSA_SIGN_PSS_2048_SHA256") -> str:
    req = SignatureRequest(key_id=key_version_name or kms_key_name(), message=message, algorithm=algorithm)
    digest = _digest(req.message, req.algorithm)
    client = get_kms_client()
    response = client.asymmetric_sign(
        request={
            "name": req.key_id,
            "digest": {"sha256": digest},
        }
    )
    return b64encode_str(response.signature)


def verify_message(message: str, signature_b64: str, key_version_name: Optional[str] = None, algorithm: str = "RSA_SIGN_PSS_2048_SHA256") -> bool:
    req = VerificationRequest(
        key_id=key_version_name or kms_key_name(),
        message=message,
        signature_b64=signature_b64,
        algorithm=algorithm,
    )
    digest = _digest(req.message, req.algorithm)
    client = get_kms_client()
    response = client.asymmetric_verify(
        request={
            "name": req.key_id,
            "digest": {"sha256": digest},
            "signature": b64decode_str(req.signature_b64),
        }
    )
    return bool(response.verified)
