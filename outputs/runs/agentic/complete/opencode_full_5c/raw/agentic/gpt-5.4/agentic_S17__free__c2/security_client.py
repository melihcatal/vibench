from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_kms_client():
    return boto3.client("kms", region_name=get_aws_region())


def get_cloudtrail_client():
    return boto3.client("cloudtrail", region_name=get_aws_region())


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def get_google_translate_headers() -> Dict[str, str]:
    return {
        "X-goog-api-key": os.environ["GOOGLE_TRANSLATE_API_KEY"],
        "Content-Type": "application/json; charset=utf-8",
    }


def post_google_translate(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        headers=get_google_translate_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def kms_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (context or {}).items()}


def aesgcm_encrypt(
    key_bytes: bytes, plaintext: bytes, aad: Optional[bytes] = None
) -> Dict[str, bytes]:
    nonce = os.urandom(12)
    cipher = AESGCM(key_bytes)
    ciphertext = cipher.encrypt(nonce, plaintext, aad)
    return {"nonce": nonce, "ciphertext": ciphertext}


def aesgcm_decrypt(
    key_bytes: bytes, nonce: bytes, ciphertext: bytes, aad: Optional[bytes] = None
) -> bytes:
    cipher = AESGCM(key_bytes)
    return cipher.decrypt(nonce, ciphertext, aad)
