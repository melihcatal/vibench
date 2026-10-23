import base64
import os
from typing import Optional

from google.cloud import kms_v1

from security_models import normalize_text_payload


def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def get_google_kms_key_name() -> str:
    key_name = os.environ.get("GOOGLE_KMS_KEY_NAME", "")
    if not key_name:
        raise ValueError("GOOGLE_KMS_KEY_NAME is required")
    return key_name


def get_google_kms_key_version_name() -> str:
    version_name = os.environ.get("GOOGLE_KMS_KEY_VERSION_NAME", "")
    if not version_name:
        raise ValueError("GOOGLE_KMS_KEY_VERSION_NAME is required")
    return version_name


def encrypt_with_google_kms(plaintext: str, key_name: Optional[str] = None, aad: Optional[str] = None) -> str:
    client = get_kms_client()
    normalized = normalize_text_payload(plaintext)
    request = kms_v1.EncryptRequest(name=key_name or get_google_kms_key_name(), plaintext=normalized.data)
    if aad is not None:
        request.additional_authenticated_data = aad.encode("utf-8")
    response = client.encrypt(request=request)
    return base64.b64encode(response.ciphertext).decode("utf-8")


def decrypt_with_google_kms(ciphertext_b64: str, key_name: Optional[str] = None, aad: Optional[str] = None) -> str:
    client = get_kms_client()
    request = kms_v1.DecryptRequest(name=key_name or get_google_kms_key_name(), ciphertext=base64.b64decode(ciphertext_b64))
    if aad is not None:
        request.additional_authenticated_data = aad.encode("utf-8")
    response = client.decrypt(request=request)
    return response.plaintext.decode("utf-8")


def sign_with_google_kms(message: str, key_version_name: Optional[str] = None) -> str:
    client = get_kms_client()
    digest = kms_v1.Digest(sha256=__import__("hashlib").sha256(message.encode("utf-8")).digest())
    response = client.asymmetric_sign(name=key_version_name or get_google_kms_key_version_name(), digest=digest)
    return base64.b64encode(response.signature).decode("utf-8")


def verify_with_google_kms(message: str, signature_b64: str, key_version_name: Optional[str] = None) -> bool:
    client = get_kms_client()
    key_version = key_version_name or get_google_kms_key_version_name()
    public_key = client.get_public_key(request={"name": key_version})
    signature = base64.b64decode(signature_b64)
    digest = kms_v1.Digest(sha256=__import__("hashlib").sha256(message.encode("utf-8")).digest())
    return client.verify_signed_digest(name=key_version, digest=digest, signature=signature, public_key=public_key).success
