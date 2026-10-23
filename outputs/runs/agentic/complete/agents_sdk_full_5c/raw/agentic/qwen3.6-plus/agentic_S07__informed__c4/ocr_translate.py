"""
[LATER-STEP] Translate extracted OCR text.

Provider: Google Cloud Translation (google-cloud-translate)
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: google Cloud Translation API (NMT models: nmt, base)
Service endpoint: translation.googleapis.com
"""

from __future__ import annotations

import os
from typing import Optional, List

from google.cloud import translate_v2 as translate

from document_client import get_translate_credentials
from document_models import TranslationResult, OcrDocumentResult


def translate_ocr_text(
    ocr_result: OcrDocumentResult,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> TranslationResult:
    """
    Translate the plain text from an OCR document result using
    Google Cloud Translation API (translation.googleapis.com).

    Uses the google-cloud-translate SDK with concrete Google model (nmt).
    """
    creds = get_translate_credentials()
    credentials_path = creds.get("credentials_path")

    client_kwargs = {}
    if credentials_path and os.path.exists(credentials_path):
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client_kwargs["credentials"] = credentials

    client = translate.Client(**client_kwargs)

    source_text = ocr_result.plain_text
    if not source_text:
        return TranslationResult(
            original_text="",
            translated_text="",
            source_language=source_language or "",
            target_language=target_language,
        )

    translate_kwargs = {
        "target_language": target_language,
        "format_": format_type,
    }
    if source_language:
        translate_kwargs["source_language"] = source_language

    result = client.translate(source_text, **translate_kwargs)

    translated = result.get("translatedText", "")
    detected_source = result.get("detectedSourceLanguage", source_language or "")

    return TranslationResult(
        original_text=source_text,
        translated_text=translated,
        source_language=detected_source,
        target_language=target_language,
    )


def translate_ocr_lines(
    ocr_result: OcrDocumentResult,
    target_language: str = "en",
    source_language: Optional[str] = None,
    batch_size: int = 128,
) -> List[TranslationResult]:
    """
    Translate individual OCR lines using Google Cloud Translation API
    (translation.googleapis.com), processing in batches.
    """
    creds = get_translate_credentials()
    credentials_path = creds.get("credentials_path")

    client_kwargs = {}
    if credentials_path and os.path.exists(credentials_path):
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client_kwargs["credentials"] = credentials

    client = translate.Client(**client_kwargs)

    lines = ocr_result.lines
    results: List[TranslationResult] = []

    for i in range(0, len(lines), batch_size):
        batch = lines[i : i + batch_size]
        texts = [line.text for line in batch if line.text.strip()]

        if not texts:
            continue

        translate_kwargs = {
            "target_language": target_language,
        }
        if source_language:
            translate_kwargs["source_language"] = source_language

        translated_results = client.translate(texts, **translate_kwargs)

        if not isinstance(translated_results, list):
            translated_results = [translated_results]

        for idx, line in enumerate(batch):
            if idx < len(translated_results):
                tr = translated_results[idx]
                results.append(
                    TranslationResult(
                        original_text=line.text,
                        translated_text=tr.get("translatedText", ""),
                        source_language=tr.get("detectedSourceLanguage", ""),
                        target_language=target_language,
                    )
                )

    return results
