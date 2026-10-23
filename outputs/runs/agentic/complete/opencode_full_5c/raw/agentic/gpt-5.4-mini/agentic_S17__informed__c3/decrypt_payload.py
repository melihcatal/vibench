import base64

from security_client import get_kms_client
from security_models import CiphertextResponse, normalize_text, b64decode_str


def decrypt_payload(ciphertext: str, key_id: str) -> CiphertextResponse:
    client = get_kms_client()
    decoded = b64decode_str(normalize_text(ciphertext))
    response = client.decrypt(CiphertextBlob=decoded, KeyId=normalize_text(key_id))
    return CiphertextResponse(
        ciphertext=response["Plaintext"].decode("utf-8", errors="replace"),
        key_id=normalize_text(key_id),
    )
