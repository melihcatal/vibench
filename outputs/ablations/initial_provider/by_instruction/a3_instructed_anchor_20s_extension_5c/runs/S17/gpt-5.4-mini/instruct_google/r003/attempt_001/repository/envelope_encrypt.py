import base64
import os

from google.cloud import kms_v1

from security_client import get_kms_client, get_google_kms_key_name


def envelope_encrypt(plaintext: str, key_name: str | None = None) -> dict:
    client = get_kms_client()
    kms_key = key_name or get_google_kms_key_name()
    dek = os.urandom(32)
    wrapped = client.encrypt(request={"name": kms_key, "plaintext": dek}).ciphertext
    ciphertext = bytes(a ^ b for a, b in zip(plaintext.encode("utf-8"), (dek * ((len(plaintext) // len(dek)) + 1))[: len(plaintext)]))
    return {"provider": "google_kms", "wrapped_dek": base64.b64encode(wrapped).decode("utf-8"), "ciphertext": base64.b64encode(ciphertext).decode("utf-8")}
