from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3
import requests

from storage_client import get_bucket_name, get_storage_config
from storage_models import StorageObjectRequest, StoredAssetSummary, normalize_object_metadata


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(slots=True)
class StoredAssetSummaryResult:
    bucket: str
    key: str
    title: str | None
    summary: str
    extracted_text: str | None = None
    language: str | None = None
    metadata: dict[str, Any] | None = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _get_object_bytes(bucket: str, key: str) -> tuple[bytes, dict[str, Any]]:
    config = get_storage_config()
    client = boto3.client(
        "s3",
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        use_ssl=config.use_ssl,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        aws_session_token=config.session_token,
    )
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read(), {
        "content_type": response.get("ContentType"),
        "content_length": response.get("ContentLength"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified"),
        "metadata": response.get("Metadata", {}),
    }


def _extract_text_from_payload(payload: dict[str, Any]) -> str:
    for field in ("extracted_text", "text", "content", "document_text", "ocr_text"):
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            return value
    raise ValueError("Missing extracted text to summarize")


def _build_messages(text: str, title: str | None, language: str | None) -> list[dict[str, str]]:
    system_parts = ["You are a concise document summarization engine."]
    if title:
        system_parts.append(f"Summarize the asset titled {title!r}.")
    if language:
        system_parts.append(f"The source language is {language}.")
    system_parts.append("Return a brief, accurate summary with key points only.")
    return [
        {"role": "system", "content": " ".join(system_parts)},
        {"role": "user", "content": text},
    ]


def summarize_stored_asset(payload: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    bucket = payload.get("bucket") or get_bucket_name()
    key = payload.get("key")
    if not isinstance(key, str) or not key:
        raise ValueError("Missing object key")

    request = StorageObjectRequest(bucket=bucket, key=key)
    extracted_text = _extract_text_from_payload(payload)
    title = payload.get("title") if isinstance(payload.get("title"), str) else None
    language = payload.get("language") if isinstance(payload.get("language"), str) else None

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(extracted_text, title, language),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = data["choices"][0]["message"]["content"]

    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    metadata = normalize_object_metadata(metadata)

    result = StoredAssetSummaryResult(
        bucket=request.bucket,
        key=request.key,
        title=title,
        summary=summary,
        extracted_text=extracted_text,
        language=language,
        metadata=metadata,
    )
    return {
        "bucket": result.bucket,
        "key": result.key,
        "title": result.title,
        "summary": result.summary,
        "extracted_text": result.extracted_text,
        "language": result.language,
        "metadata": result.metadata or {},
        "provider": "openai",
        "model": OPENAI_MODEL,
    }


def summarize_stored_asset_object(bucket: str | None, key: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    payload.setdefault("bucket", bucket or get_bucket_name())
    payload["key"] = key
    if "extracted_text" not in payload:
        _, metadata = _get_object_bytes(payload["bucket"], key)
        payload.setdefault("metadata", metadata)
        payload.setdefault("extracted_text", "")
    return summarize_stored_asset(payload)
