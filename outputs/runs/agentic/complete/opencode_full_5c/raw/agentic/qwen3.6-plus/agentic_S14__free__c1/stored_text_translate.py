from __future__ import annotations

from typing import Optional

from storage_client import get_translate_client, get_object_content, get_s3_client
from storage_models import (
    TranslateRequest,
    TranslateResponse,
    normalize_translate_response,
)


def translate_stored_document_text(
    bucket: str,
    key: str,
    target_language: str = "en",
    source_language: str = "auto",
    version_id: Optional[str] = None,
    translate_client=None,
    s3_client=None,
) -> TranslateResponse:
    if s3_client is None:
        s3_client = get_s3_client()
    if translate_client is None:
        translate_client = get_translate_client()

    document_bytes = get_object_content(bucket, key, version_id, client=s3_client)
    text_content = document_bytes.decode("utf-8", errors="replace")

    request = TranslateRequest(
        text=text_content,
        source_language=source_language,
        target_language=target_language,
    )

    params = {
        "Text": text_content,
        "TargetLanguageCode": target_language,
    }
    if source_language and source_language != "auto":
        params["SourceLanguageCode"] = source_language

    response = translate_client.translate_text(**params)

    return normalize_translate_response(response, request)


def batch_translate_stored_text(
    texts: list[str],
    target_language: str = "en",
    source_language: str = "auto",
    translate_client=None,
) -> list[TranslateResponse]:
    if translate_client is None:
        translate_client = get_translate_client()

    results = []
    for text in texts:
        params = {
            "Text": text,
            "TargetLanguageCode": target_language,
        }
        if source_language and source_language != "auto":
            params["SourceLanguageCode"] = source_language

        response = translate_client.translate_text(**params)

        request = TranslateRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        results.append(normalize_translate_response(response, request))

    return results
