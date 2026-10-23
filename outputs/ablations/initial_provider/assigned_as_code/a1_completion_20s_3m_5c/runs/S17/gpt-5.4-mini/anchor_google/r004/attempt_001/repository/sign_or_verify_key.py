from google.cloud import kms

from security_client import crypto_key_version_path, load_config


def sign_or_verify_key(payload, config=None):
    config = load_config(config)
    client = kms.KeyManagementServiceClient()
    name = crypto_key_version_path(config)
    if payload.get("signature"):
        result = client.asymmetric_sign(request={"name": name, "digest": payload["digest"]})
        return {"signature": result.signature}
    verified = client.asymmetric_verify(request={"name": name, "digest": payload["digest"], "signature": payload["signature"]})
    return {"verified": verified.success}
