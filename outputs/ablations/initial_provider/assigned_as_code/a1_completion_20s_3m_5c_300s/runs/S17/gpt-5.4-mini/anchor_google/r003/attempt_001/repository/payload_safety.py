from google.cloud import kms


def payload_safety(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    client.get_crypto_key(request={"name": name})
    text = payload.get("plaintext", b"")
    unsafe = b"secret" in text.lower() or b"password" in text.lower()
    return {"unsafe": unsafe}
