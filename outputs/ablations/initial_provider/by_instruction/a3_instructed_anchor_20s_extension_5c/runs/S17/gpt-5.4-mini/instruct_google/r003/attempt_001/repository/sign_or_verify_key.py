from security_client import sign_with_google_kms, verify_with_google_kms


def sign_or_verify_key(message: str, signature_b64: str | None = None, key_version_name: str | None = None) -> dict:
    if signature_b64 is None:
        return {"provider": "google_kms", "mode": "sign", "signature": sign_with_google_kms(message, key_version_name)}
    return {"provider": "google_kms", "mode": "verify", "valid": verify_with_google_kms(message, signature_b64, key_version_name)}
