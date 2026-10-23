import base64
import os

from security_client import get_kms_client, get_key_id
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(ciphertext: str, key_id: str | None = None) -> DecryptResponse:
    client = get_kms_client()
    resolved_key_id = key_id or get_key_id()
    request = DecryptRequest(ciphertext=ciphertext, key_id=resolved_key_id)
    response = client.decrypt(CiphertextBlob=base64.b64decode(request.ciphertext.encode("ascii")))
    plaintext = response["Plaintext"].decode("utf-8")
    return DecryptResponse(plaintext=plaintext, key_id=resolved_key_id, provider="aws-kms")


if __name__ == "__main__":
    payload = os.environ.get("CIPHERTEXT_PAYLOAD", "")
    result = decrypt_payload(payload)
    print(result.plaintext)
