import base64

from security_client import kms_client, load_security_config, normalize_payload
from security_models import CiphertextResponse, PayloadRequest, normalize_metadata


def encrypt_payload(
    plaintext: str, key_id: str = "", metadata=None
) -> CiphertextResponse:
    cfg = load_security_config()
    request = PayloadRequest(
        plaintext=normalize_payload(plaintext),
        key_id=key_id or cfg["kms_key_id"],
        metadata=metadata,
    )
    client = kms_client()
    response = client.encrypt(
        KeyId=request.key_id, Plaintext=request.plaintext.encode("utf-8")
    )
    ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("utf-8")
    return CiphertextResponse(
        ciphertext=ciphertext,
        key_id=request.key_id,
        metadata=normalize_metadata(request.metadata),
    )
