from google.cloud import kms

from security_client import build_kms_request


def decrypt_payload(payload, config=None):
    client = kms.KeyManagementServiceClient()
    request = build_kms_request(config, ciphertext=payload["ciphertext"])
    response = client.decrypt(request=request)
    return {"plaintext": response.plaintext}
