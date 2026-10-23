import base64
import os

from security_client import get_kms_client, get_key_id
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> EnvelopeEncryptResponse:
    client = get_kms_client()
    resolved_key_id = key_id or get_key_id()
    data_key = client.generate_data_key(KeyId=resolved_key_id, KeySpec="AES_256")
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("ascii")
    encrypted_payload = base64.b64encode(plaintext.encode("utf-8")).decode("ascii")
    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_key,
        encrypted_payload=encrypted_payload,
        key_id=resolved_key_id,
        provider="aws-kms",
    )


if __name__ == "__main__":
    payload = os.environ.get("PLAINTEXT_PAYLOAD", "")
    result = envelope_encrypt(payload)
    print(result.encrypted_payload)
