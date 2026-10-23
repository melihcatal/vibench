import base64

from security_client import kms_client, normalize_payload
from security_models import CiphertextResponse, normalize_metadata


def decrypt_payload(
    ciphertext: str, key_id: str = "", metadata=None
) -> CiphertextResponse:
    client = kms_client()
    blob = base64.b64decode(normalize_payload(ciphertext))
    response = client.decrypt(CiphertextBlob=blob, KeyId=key_id or None)
    plaintext = response["Plaintext"].decode("utf-8")
    return CiphertextResponse(
        ciphertext=plaintext,
        key_id=response.get("KeyId", key_id),
        metadata=normalize_metadata(metadata),
    )
