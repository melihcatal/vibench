import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class StoredTextTranslateResult:
    bucket: str
    key: str
    source_language: Optional[str]
    target_language: str
    translated_text: str
    model_id: str
    raw: Optional[Dict[str, Any]] = None


def _textract_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
    }
    if region:
        kwargs["region_name"] = region
    return boto3.client("textract", **kwargs)


def _translate_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
    }
    if region:
        kwargs["region_name"] = region
    return boto3.client("translate", **kwargs)


def _extract_text(bucket: str, key: str) -> str:
    response = _textract_client().detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            text = block.get("Text")
            if text:
                lines.append(text)
    return "\n".join(lines)


def translate_stored_text(
    bucket: str,
    key: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> StoredTextTranslateResult:
    text = _extract_text(bucket, key)
    translate_kwargs: Dict[str, Any] = {"Text": text, "TargetLanguageCode": target_language}
    if source_language:
        translate_kwargs["SourceLanguageCode"] = source_language
    response = _translate_client().translate_text(**translate_kwargs)
    return StoredTextTranslateResult(
        bucket=bucket,
        key=key,
        source_language=response.get("SourceLanguageCode") or source_language,
        target_language=response.get("TargetLanguageCode") or target_language,
        translated_text=response.get("TranslatedText") or "",
        model_id="amazon-translate",
        raw=response,
    )


__all__ = ["StoredTextTranslateResult", "translate_stored_text"]
