from google.cloud import kms

from security_client import load_config


def decrypt_payload(payload, config=None):
    config = load_config(config)
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.decrypt(request={"name": name, "ciphertext": payload["ciphertext"]})
    return {"plaintext": response.plaintext}
