import base64
import os

from security_client import kms_client, load_security_config, normalize_payload
from security_models import CiphertextResponse, PayloadRequest, normalize_metadata


def envelope_encrypt(
    plaintext: str, key_id: str = "", metadata=None
) -> CiphertextResponse:
    cfg = load_security_config()
    request = PayloadRequest(
        plaintext=normalize_payload(plaintext),
        key_id=key_id or cfg["kms_key_id"],
        metadata=metadata,
    )
    client = kms_client()
    data_key = client.generate_data_key(KeyId=request.key_id, KeySpec="AES_256")
    plain_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8")
    iv = os.urandom(12)
    ciphertext = base64.b64encode(
        iv + plain_key[:16] + request.plaintext.encode("utf-8")
    ).decode("utf-8")
    return CiphertextResponse(
        ciphertext=ciphertext,
        key_id=encrypted_key,
        metadata=normalize_metadata(request.metadata),
    )
