import base64

from security_client import decrypt_aead_ciphertext


def decrypt_payload(ciphertext_b64: str, aad: str = "") -> str:
    return decrypt_aead_ciphertext(base64.b64decode(ciphertext_b64), aad.encode("utf-8")).get("plaintext", "")
