from google.cloud import kms

def summarize_key_usage(config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.get_crypto_key(request={"name": name})
    return {"usage": response.usage}