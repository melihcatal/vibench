from google.cloud import kms


def envelope_encrypt(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    dek = payload["data_key"]
    encrypted_dek = client.encrypt(request={"name": name, "plaintext": dek}).ciphertext
    return {"encrypted_data_key": encrypted_dek, "encrypted_payload": payload["encrypted_payload"]}
