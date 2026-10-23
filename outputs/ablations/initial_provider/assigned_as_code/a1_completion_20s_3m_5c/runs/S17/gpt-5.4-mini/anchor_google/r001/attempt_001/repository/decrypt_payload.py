from google.cloud import kms

from security_client import load_security_config, crypto_key_name, normalize_ciphertext


def decrypt_payload(payload, config=None):
    config = load_security_config(config)
    client = kms.KeyManagementServiceClient()
    name = crypto_key_name(config)
    response = client.decrypt(request={"name": name, "ciphertext": normalize_ciphertext(payload)})
    return {"plaintext": response.plaintext}
