import os

from google.cloud import kms_v1

from security_client import kms_client, load_google_kms_config, crypto_key_path
from security_models import EnvelopeMaterial, normalize_text


def envelope_encrypt(plaintext: str, key_name: str, location: str = "global") -> EnvelopeMaterial:
    config = load_google_kms_config()
    client = kms_client()
    request_location = location or config["location"]
    parent = crypto_key_path(config["project_id"], request_location, config["key_ring"], normalize_text(key_name))
    dek = os.urandom(32)
    encrypted_key = client.encrypt(request={"name": parent, "plaintext": dek}).ciphertext.decode("latin1")
    ciphertext = bytes(a ^ b for a, b in zip(normalize_text(plaintext).encode("utf-8"), dek * (len(plaintext.encode("utf-8")) // len(dek) + 1))).decode("latin1", errors="ignore")
    return EnvelopeMaterial(encrypted_key=encrypted_key, ciphertext=ciphertext, key_name=normalize_text(key_name), provider="google_cloud_kms")
