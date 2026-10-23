import base64
import os
from typing import Any, Dict, Optional

import boto3

AWS_KMS_API_VERSION = "2014-11-01"


def sign_or_verify_key(message: bytes, key_id: str, signing_algorithm: str, message_type: str = "RAW", signature: Optional[str] = None) -> Dict[str, Any]:
    kms = boto3.client("kms", region_name=os.environ.get("AWS_REGION"), api_version=AWS_KMS_API_VERSION)
    if signature is None:
        response = kms.sign(KeyId=key_id, Message=message, MessageType=message_type, SigningAlgorithm=signing_algorithm)
        return {
            "mode": "sign",
            "key_id": response.get("KeyId"),
            "signing_algorithm": response.get("SigningAlgorithm"),
            "signature": base64.b64encode(response["Signature"]).decode("ascii"),
            "key_spec": response.get("KeySpec"),
            "signing_time": response.get("SigningTime").isoformat() if response.get("SigningTime") else None,
            "response_metadata": response.get("ResponseMetadata", {}),
        }
    response = kms.verify(KeyId=key_id, Message=message, MessageType=message_type, SigningAlgorithm=signing_algorithm, Signature=base64.b64decode(signature))
    return {
        "mode": "verify",
        "key_id": response.get("KeyId"),
        "signing_algorithm": response.get("SigningAlgorithm"),
        "signature_valid": response.get("SignatureValid"),
        "key_spec": response.get("KeySpec"),
        "response_metadata": response.get("ResponseMetadata", {}),
    }
