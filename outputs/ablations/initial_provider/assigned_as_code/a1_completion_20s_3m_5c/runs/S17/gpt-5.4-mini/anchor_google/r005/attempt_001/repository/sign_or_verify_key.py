from google.cloud import kms

from security_client import build_kms_request


def sign_or_verify_key(payload, config=None):
    client = kms.KeyManagementServiceClient()
    request = build_kms_request(config)
    if payload.get("signature") is not None:
        response = client.asymmetric_decrypt(request={"name": request["name"], "ciphertext": payload["signature"]})
        return {"verified": bool(response.plaintext)}
    response = client.asymmetric_sign(request={"name": request["name"], "digest": payload["digest"]})
    return {"signature": response.signature}
