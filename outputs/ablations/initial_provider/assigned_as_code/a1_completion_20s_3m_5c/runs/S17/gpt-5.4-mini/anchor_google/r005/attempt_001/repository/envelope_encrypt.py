from google.cloud import kms

from security_client import build_kms_request


def envelope_encrypt(payload, config=None):
    client = kms.KeyManagementServiceClient()
    key_request = build_kms_request(config)
    public_key = client.get_public_key(request=key_request)
    response = client.encrypt(request={"name": key_request["name"], "plaintext": payload["plaintext"]})
    return {"ciphertext": response.ciphertext, "public_key_pem": public_key.pem}
