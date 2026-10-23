from google.cloud import kms


def decrypt_payload(ciphertext, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.decrypt(request={"name": name, "ciphertext": ciphertext["ciphertext"]})
    return {"plaintext": response.plaintext}