from google.cloud import kms

from security_client import load_security_config, crypto_key_version_name, normalize_plaintext, normalize_ciphertext


def sign_or_verify_key(payload, config=None):
    config = load_security_config(config)
    client = kms.KeyManagementServiceClient()
    if payload.get("mode") == "verify":
        name = crypto_key_version_name(config)
        response = client.asymmetric_verify(request={"name": name, "digest": payload.get("digest", {}), "signature": normalize_ciphertext(payload)})
        return {"verified": response.success}
    name = crypto_key_version_name(config)
    response = client.asymmetric_sign(request={"name": name, "digest": payload.get("digest", {})})
    return {"signature": response.signature}
