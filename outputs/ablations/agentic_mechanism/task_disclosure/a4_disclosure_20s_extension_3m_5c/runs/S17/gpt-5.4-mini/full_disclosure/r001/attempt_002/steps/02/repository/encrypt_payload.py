import base64
import json
import os
from typing import Any, Dict, Optional

import boto3

AWS_KMS_API_VERSION = "2014-11-01"


def encrypt_payload(plaintext: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    kms = boto3.client("kms", region_name=os.environ.get("AWS_REGION"), api_version=AWS_KMS_API_VERSION)
    params: Dict[str, Any] = {"Plaintext": plaintext.encode("utf-8")}
    if key_id:
        params["KeyId"] = key_id
    if encryption_context:
        params["EncryptionContext"] = encryption_context
    response = kms.encrypt(**params)
    return {
        "key_id": response.get("KeyId"),
        "ciphertext_blob": base64.b64encode(response["CiphertextBlob"]).decode("ascii"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
        "response_metadata": response.get("ResponseMetadata", {}),
    }


def encrypt_payload_json(plaintext: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> str:
    return json.dumps(encrypt_payload(plaintext, key_id=key_id, encryption_context=encryption_context))
