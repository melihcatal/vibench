import base64
from typing import Any, Dict

import boto3

from security_models import EncryptRequest, EncryptResponse, normalize_text


def encrypt_payload(plaintext: str, key_id: str) -> Dict[str, Any]:
    client = boto3.client("kms")
    request = EncryptRequest(plaintext=normalize_text(plaintext), key_id=key_id)
    response = client.encrypt(KeyId=request.key_id, Plaintext=request.plaintext.encode("utf-8"))
    ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("utf-8")
    return EncryptResponse(provider="aws-kms", key_id=key_id, ciphertext=ciphertext).to_dict()
