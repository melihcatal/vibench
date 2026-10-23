import base64

from google.cloud import kms_v1

from security_client import kms_client, kms_key_name, load_security_config
from security_models import normalize_payload_request


def encrypt_payload(payload: str, aad: str = "") -> str:
    config = load_security_config()
    client = kms_client()
    request = normalize_payload_request({"payload": payload, "aad": aad})
    response = client.encrypt(
        request={
            "name": kms_key_name(config),
            "plaintext": request.payload.encode("utf-8"),
            "additional_authenticated_data": (request.aad or "").encode("utf-8"),
        }
    )
    return base64.b64encode(response.ciphertext).decode("ascii")


if __name__ == "__main__":
    print(encrypt_payload("hello"))
