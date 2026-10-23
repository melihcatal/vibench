from google.cloud import kms

from security_client import crypto_key_path, load_config


def envelope_encrypt(payload, config=None):
    config = load_config(config)
    client = kms.KeyManagementServiceClient()
    name = crypto_key_path(config)
    dek = payload.get("data_encryption_key", b"")
    encrypted_dek = client.encrypt(request={"name": name, "plaintext": dek})
    return {"encrypted_dek": encrypted_dek.ciphertext, "ciphertext": payload.get("ciphertext", b"")}
