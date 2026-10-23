import base64
import os

import boto3

from security_client import get_kms_client, get_key_id
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(plaintext: str, key_id: str | None = None) -> EncryptResponse:
    client = get_kms_client()
    resolved_key_id = key_id or get_key_id()
    request = EncryptRequest(plaintext=plaintext, key_id=resolved_key_id)
    response = client.encrypt(KeyId=request.key_id, Plaintext=request.plaintext.encode("utf-8"))
    ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("ascii")
    return EncryptResponse(ciphertext=ciphertext, key_id=resolved_key_id, provider="aws-kms")


if __name__ == "__main__":
    payload = os.environ.get("PLAINTEXT_PAYLOAD", "")
    result = encrypt_payload(payload)
    print(result.ciphertext)
