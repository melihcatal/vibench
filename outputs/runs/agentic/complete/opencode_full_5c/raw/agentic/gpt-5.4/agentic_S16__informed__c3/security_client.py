from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import boto3
from anthropic import Anthropic
from deepl import Translator
from openai import OpenAI
import requests

from security_models import SecretPayload


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def secrets_manager_client():
    return boto3.client("secretsmanager", region_name=aws_region())


def fetch_secret_value(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretPayload:
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage
    response = secrets_manager_client().get_secret_value(**params)
    secret_string = response.get("SecretString")
    if secret_string is None:
        binary_value = response.get("SecretBinary", b"")
        secret_string = (
            binary_value.decode("utf-8")
            if isinstance(binary_value, (bytes, bytearray))
            else str(binary_value)
        )
    stages = response.get("VersionStages") or []
    return SecretPayload(
        name=secret_id,
        value=secret_string,
        version_id=response.get("VersionId"),
        version_stage=stages[0] if stages else None,
        metadata={
            "arn": response.get("ARN"),
            "created_date": response.get("CreatedDate").isoformat()
            if response.get("CreatedDate")
            else None,
            "version_stages": stages,
        },
    )


def parse_secret_json(payload: SecretPayload) -> SecretPayload:
    parsed = json.loads(payload.value)
    payload.parsed_json = parsed
    return payload


def get_secret_metadata(secret_id: str) -> Dict[str, Any]:
    response = secrets_manager_client().describe_secret(SecretId=secret_id)
    last_rotated = response.get("LastRotatedDate")
    return {
        "arn": response.get("ARN"),
        "name": response.get("Name"),
        "description": response.get("Description"),
        "last_rotated_date": last_rotated.isoformat() if last_rotated else None,
        "rotation_enabled": response.get("RotationEnabled"),
        "version_ids_to_stages": response.get("VersionIdsToStages") or {},
        "tags": response.get("Tags") or [],
    }


def anthropic_client() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def summarize_text(text: str) -> str:
    response = anthropic_client().messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": text}],
    )
    return "".join(
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text"
    ).strip()


def perspective_analyze(text: str) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
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


def openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_text(text: str) -> Dict[str, Any]:
    response = openai_client().embeddings.create(
        model="text-embedding-3-large", input=text
    )
    item = response.data[0]
    return {"embedding": item.embedding, "model": response.model}


def deepl_translator() -> Translator:
    return Translator(os.environ["DEEPL_AUTH_KEY"])


def translate_text(text: str, target_language: str) -> Dict[str, Any]:
    result = deepl_translator().translate_text(text, target_lang=target_language)
    return {
        "text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", None),
    }
