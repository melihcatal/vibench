from google.cloud import kms

def envelope_encrypt(data_key, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.encrypt(request={"name": name, "plaintext": data_key})
    return {"encrypted_data_key": response.ciphertext}