from google.cloud import kms


def encrypt_payload(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.encrypt(request={"name": name, "plaintext": payload["plaintext"]})
    return {"ciphertext": response.ciphertext}
