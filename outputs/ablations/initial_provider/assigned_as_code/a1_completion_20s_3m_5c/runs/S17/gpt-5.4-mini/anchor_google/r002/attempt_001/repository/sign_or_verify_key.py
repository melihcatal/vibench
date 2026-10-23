from google.cloud import kms


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_version_path(config["project_id"], config["location"], config["key_ring"], config["key_id"], config.get("version", "1"))
    if payload.get("operation") == "sign":
        response = client.asymmetric_sign(request={"name": name, "digest": payload["digest"]})
        return {"signature": response.signature}
    response = client.asymmetric_verify(request={"name": name, "digest": payload["digest"], "signature": payload["signature"]})
    return {"verified": response.success}
