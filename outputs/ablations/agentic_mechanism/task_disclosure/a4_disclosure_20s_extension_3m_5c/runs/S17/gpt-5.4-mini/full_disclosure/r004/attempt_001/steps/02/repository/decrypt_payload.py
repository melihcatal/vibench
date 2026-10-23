import base64
import json
import os
from typing import Any, Dict, Optional

import requests


AWS_KMS_DECRYPT_URL = "https://kms.{region}.amazonaws.com/"


def _signing_headers(target: str, payload: str, region: str, service: str = "kms") -> Dict[str, str]:
    raise NotImplementedError("AWS SigV4 signing is required for live requests")


def decrypt_payload(ciphertext_b64: str, region: Optional[str] = None) -> str:
    region = region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not region:
        raise ValueError("AWS region must be provided via region or AWS_REGION/AWS_DEFAULT_REGION")

    endpoint = AWS_KMS_DECRYPT_URL.format(region=region)
    body = {
        "CiphertextBlob": ciphertext_b64,
    }

    headers = {
        "content-type": "application/x-amz-json-1.1",
        "x-amz-target": "TrentService.Decrypt",
    }
    headers.update(_signing_headers("TrentService.Decrypt", json.dumps(body), region))

    response = requests.post(endpoint, headers=headers, data=json.dumps(body), timeout=30)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    plaintext = data.get("Plaintext")
    if not plaintext:
        raise ValueError("AWS KMS response did not include Plaintext")
    if isinstance(plaintext, str):
        return base64.b64decode(plaintext).decode("utf-8")
    return base64.b64decode(plaintext).decode("utf-8")
