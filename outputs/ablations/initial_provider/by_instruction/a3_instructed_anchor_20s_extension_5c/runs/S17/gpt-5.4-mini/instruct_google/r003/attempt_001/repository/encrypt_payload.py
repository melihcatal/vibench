import base64

from security_client import encrypt_with_google_kms


def encrypt_payload(plaintext: str, key_name: str | None = None, aad: str | None = None) -> dict:
    ciphertext = encrypt_with_google_kms(plaintext=plaintext, key_name=key_name, aad=aad)
    return {"provider": "google_kms", "ciphertext": ciphertext, "encoding": "base64"}


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else ""
    result = encrypt_payload(text)
    print(base64.b64encode(result["ciphertext"].encode("utf-8")).decode("utf-8"))
