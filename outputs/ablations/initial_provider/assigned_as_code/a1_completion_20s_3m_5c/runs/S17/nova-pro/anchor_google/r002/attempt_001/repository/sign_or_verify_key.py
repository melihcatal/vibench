from google.cloud import kms


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    response = client.asymmetric_sign(request={"name": name, "digest": {"sha256": payload}})
    return {"signature": response.signature}