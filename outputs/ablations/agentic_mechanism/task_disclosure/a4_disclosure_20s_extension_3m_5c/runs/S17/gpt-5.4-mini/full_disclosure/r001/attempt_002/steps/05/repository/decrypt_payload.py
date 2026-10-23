import base64
import json
import os
from typing import Any, Dict, Optional

import boto3

AWS_KMS_API_VERSION = "2014-11-01"


def decrypt_payload(ciphertext_blob: str, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    kms = boto3.client("kms", region_name=os.environ.get("AWS_REGION"), api_version=AWS_KMS_API_VERSION)
    params: Dict[str, Any] = {"CiphertextBlob": base64.b64decode(ciphertext_blob)}
    if encryption_context:
        params["EncryptionContext"] = encryption_context
    response = kms.decrypt(**params)
    plaintext = response["Plaintext"].decode("utf-8")
    return {
        "plaintext": plaintext,
        "key_id": response.get("KeyId"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
        "response_metadata": response.get("ResponseMetadata", {}),
    }


def decrypt_payload_json(ciphertext_blob: str, encryption_context: Optional[Dict[str, str]] = None) -> str:
    return json.dumps(decrypt_payload(ciphertext_blob, encryption_context=encryption_context))
