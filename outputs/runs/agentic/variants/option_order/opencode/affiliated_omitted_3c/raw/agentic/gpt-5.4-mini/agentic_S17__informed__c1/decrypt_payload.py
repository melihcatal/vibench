import base64
import json
from typing import Any, Dict

import boto3

from security_models import DecryptRequest, DecryptResponse, normalize_ciphertext


def decrypt_payload(ciphertext: str, key_id: str) -> Dict[str, Any]:
    client = boto3.client("kms")
    request = DecryptRequest(ciphertext=normalize_ciphertext(ciphertext), key_id=key_id)
    response = client.decrypt(CiphertextBlob=base64.b64decode(request.ciphertext))
    plaintext = response["Plaintext"].decode("utf-8")
    return DecryptResponse(provider="aws-kms", key_id=key_id, plaintext=plaintext).to_dict()
