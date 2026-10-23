from __future__ import annotations

import os
from typing import Dict, Optional

import boto3
from botocore.config import Config
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI
import requests
import cohere
import deepl


AWS_KMS_PROVIDER = "aws-kms"
OPENAI_PROVIDER = "openai"
PERSPECTIVE_PROVIDER = "perspective-api"
COHERE_PROVIDER = "cohere"
DEEPL_PROVIDER = "deepl"
AWS_KMS_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"
COHERE_EMBED_MODEL = "embed-english-v3.0"


def get_aws_region() -> str:
    return (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )


def get_kms_client():
    return boto3.client(
        "kms",
        region_name=get_aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def get_perspective_api_key() -> str:
    return os.environ["PERSPECTIVE_API_KEY"]


def get_perspective_endpoint() -> str:
    return "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_cohere_client() -> cohere.ClientV2:
    return cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])


def get_deepl_client() -> deepl.Translator:
    return deepl.Translator(os.environ["DEEPL_AUTH_KEY"])


def aesgcm_encrypt(
    key: bytes, plaintext: bytes, associated_data: Optional[bytes] = None
) -> Dict[str, bytes]:
    nonce = os.urandom(12)
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, plaintext, associated_data)
    return {"nonce": nonce, "ciphertext": ciphertext}


def aesgcm_decrypt(
    key: bytes, nonce: bytes, ciphertext: bytes, associated_data: Optional[bytes] = None
) -> bytes:
    cipher = AESGCM(key)
    return cipher.decrypt(nonce, ciphertext, associated_data)


def normalized_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    return dict(sorted((context or {}).items(), key=lambda item: item[0]))


def perspective_analyze(text: str) -> Dict:
    response = requests.post(
        get_perspective_endpoint(),
        params={"key": get_perspective_api_key()},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
