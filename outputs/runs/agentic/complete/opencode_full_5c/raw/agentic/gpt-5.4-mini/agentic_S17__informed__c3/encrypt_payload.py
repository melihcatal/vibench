import base64

from security_client import get_kms_client
from security_models import PayloadRequest, CiphertextResponse, normalize_text


def encrypt_payload(plaintext: str, key_id: str) -> CiphertextResponse:
    client = get_kms_client()
    req = PayloadRequest(
        plaintext=normalize_text(plaintext), key_id=normalize_text(key_id)
    )
    response = client.encrypt(KeyId=req.key_id, Plaintext=req.plaintext.encode("utf-8"))
    return CiphertextResponse(
        ciphertext=base64.b64encode(response["CiphertextBlob"]).decode("ascii"),
        key_id=req.key_id,
    )
