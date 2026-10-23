import base64
import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _load_payload(value: str) -> bytes:
    try:
        data = json.loads(value)
        if isinstance(data, dict):
            value = data.get("CiphertextBlob") or data.get("ciphertext") or data.get("payload") or value
    except json.JSONDecodeError:
        pass
    return base64.b64decode(value)


def decrypt_payload() -> Dict[str, Any]:
    ciphertext = os.environ["CIPHERTEXT_B64"]
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    region = os.environ.get("AWS_REGION")

    client_kwargs: Dict[str, Any] = {}
    if region:
        client_kwargs["region_name"] = region

    kms = boto3.client("kms", **client_kwargs)
    params: Dict[str, Any] = {"CiphertextBlob": _load_payload(ciphertext)}
    if key_id:
        params["KeyId"] = key_id

    try:
        response = kms.decrypt(**params)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"AWS KMS decrypt failed: {exc}") from exc

    plaintext = response["Plaintext"]
    result: Dict[str, Any] = {
        "plaintext_b64": base64.b64encode(plaintext).decode("utf-8"),
        "plaintext": plaintext.decode("utf-8", errors="replace"),
        "key_id": response.get("KeyId"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
        "provider": "aws_kms",
    }
    return result


if __name__ == "__main__":
    print(json.dumps(decrypt_payload()))
