from security_client import decrypt_with_google_kms


def decrypt_payload(ciphertext_b64: str, key_name: str | None = None, aad: str | None = None) -> dict:
    plaintext = decrypt_with_google_kms(ciphertext_b64=ciphertext_b64, key_name=key_name, aad=aad)
    return {"provider": "google_kms", "plaintext": plaintext}
