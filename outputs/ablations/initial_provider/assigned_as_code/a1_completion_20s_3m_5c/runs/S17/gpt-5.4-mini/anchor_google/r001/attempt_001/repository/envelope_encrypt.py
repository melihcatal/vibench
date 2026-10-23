from google.cloud import kms

from security_client import load_security_config, crypto_key_name, normalize_plaintext


def envelope_encrypt(payload, config=None):
    config = load_security_config(config)
    client = kms.KeyManagementServiceClient()
    name = crypto_key_name(config)
    response = client.encrypt(request={"name": name, "plaintext": normalize_plaintext(payload)})
    return {"ciphertext": response.ciphertext, "wrapped_key": response.ciphertext}
