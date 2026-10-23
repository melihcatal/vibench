import base64
import json
import os
from typing import Any, Dict, Optional

import requests


AWS_REGION_ENV = "AWS_REGION"
AWS_KEY_ID_ENV = "AWS_KMS_KEY_ID"
AWS_ACCESS_KEY_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
AWS_SESSION_TOKEN_ENV = "AWS_SESSION_TOKEN"


def _aws_session() -> requests.Session:
    session = requests.Session()
    access_key = os.getenv(AWS_ACCESS_KEY_ENV)
    secret_key = os.getenv(AWS_SECRET_KEY_ENV)
    session_token = os.getenv(AWS_SESSION_TOKEN_ENV)
    if access_key:
        session.headers["X-Aws-Access-Key-Id"] = access_key
    if secret_key:
        session.headers["X-Aws-Secret-Access-Key"] = secret_key
    if session_token:
        session.headers["X-Aws-Session-Token"] = session_token
    return session


def _kms_endpoint(region: str) -> str:
    return f"https://kms.{region}.amazonaws.com/"


def _aws_target(action: str) -> str:
    return f"TrentService.{action}"


def _request(action: str, payload: Dict[str, Any], region: str) -> Dict[str, Any]:
    session = _aws_session()
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": _aws_target(action),
    }
    response = session.post(_kms_endpoint(region), headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    return response.json()


def sign_message(message: bytes, key_id: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    region = region or os.getenv(AWS_REGION_ENV, "us-east-1")
    key_id = key_id or os.getenv(AWS_KEY_ID_ENV)
    if not key_id:
        raise ValueError("AWS KMS key id is required")
    payload = {
        "KeyId": key_id,
        "Message": base64.b64encode(message).decode("ascii"),
        "MessageType": "RAW",
        "SigningAlgorithm": "RSASSA_PSS_SHA_256",
    }
    result = _request("Sign", payload, region)
    return {
        "key_id": key_id,
        "region": region,
        "signing_algorithm": result.get("SigningAlgorithm"),
        "signature": result.get("Signature"),
    }


def verify_signature(message: bytes, signature: str, key_id: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    region = region or os.getenv(AWS_REGION_ENV, "us-east-1")
    key_id = key_id or os.getenv(AWS_KEY_ID_ENV)
    if not key_id:
        raise ValueError("AWS KMS key id is required")
    payload = {
        "KeyId": key_id,
        "Message": base64.b64encode(message).decode("ascii"),
        "MessageType": "RAW",
        "Signature": signature,
        "SigningAlgorithm": "RSASSA_PSS_SHA_256",
    }
    result = _request("Verify", payload, region)
    return {
        "key_id": key_id,
        "region": region,
        "signature_valid": result.get("SignatureValid", False),
        "signing_algorithm": result.get("SigningAlgorithm"),
    }


def sign_or_verify_key(payload: bytes, signature: Optional[str] = None, key_id: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    if signature is None:
        return sign_message(payload, key_id=key_id, region=region)
    return verify_signature(payload, signature=signature, key_id=key_id, region=region)
