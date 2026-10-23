import base64

from security_client import kms_client, load_config
from security_models import PayloadRequest, ensure_text


def encrypt_payload(payload: str, key_id: str | None = None) -> dict:
    config = load_config()
    client = kms_client(config)
    request = PayloadRequest(
        payload=ensure_text(payload), key_id=key_id or config.key_id
    )
    response = client.encrypt(
        KeyId=request.key_id, Plaintext=request.payload.encode("utf-8")
    )
    return {
        "key_id": request.key_id,
        "ciphertext": base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
    }
