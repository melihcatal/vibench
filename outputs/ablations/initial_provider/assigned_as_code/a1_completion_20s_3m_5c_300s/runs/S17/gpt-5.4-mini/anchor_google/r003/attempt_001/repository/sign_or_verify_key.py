from google.cloud import kms


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_version_path(config["project_id"], config["location"], config["key_ring"], config["key_id"], config.get("version", "1"))
    if payload.get("mode") == "verify":
        response = client.verify_attestation(request={"name": name, "attestation": payload["signature"]})
        return {"verified": bool(response.name)}
    response = client.asymmetric_sign(request={"name": name, "digest": payload["digest"]})
    return {"signature": response.signature}
