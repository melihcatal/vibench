from storage_client import ManagedClient
from storage_models import ObjectInfo, OCRResult, TranslationResult, AssetSummary
import re
from typing import Dict, Optional


def summarize_stored_asset(bucket_name: str, object_key: str) -> AssetSummary:
    """Create a concise summary of a stored document by combining metadata, OCR text, and translation.

    The function:
    1. Reads the object's metadata (size, last‑modified).
    2. Extracts plain text with Alibaba Cloud OCR.
    3. Generates an English translation of the OCR output.
    4. Builds a short summary (first 2 sentences of the translated text).

    Returns an AssetSummary instance.
    """
    client = ManagedClient()
    # 1. Metadata
    meta = client.head_object(
        bucket_name, object_key
    )  # dict-like; extract useful fields
    size = meta.get("ContentLength")
    last_mod = meta.get("LastModified")
    # 2. OCR (assumes the object is a PDF, image, etc.)
    ocr = ocr_stored_document(bucket_name, object_key)
    # 3. Translate the OCR result to English
    translation = translate_text(
        TranslationRequest(source_text=ocr.text, target_lang="en")
    )
    raw_text = translation.translated_text
    # Very naive summarization: take first two sentences
    sentences = re.split(r"(?<=[.!?])\s+", raw_text)
    summary_sentences = sentences[:2]
    summary = " ".join(summary_sentences)
    # 4. Assemble summary object
    return AssetSummary(
        title=f"Document: {object_key[-30:]}",
        summary=summary,
        metadata={
            "bucket": bucket_name,
            "object_key": object_key,
            "size_bytes": size,
            "last_modified": str(last_mod) if last_mod else None,
            "ocr_language": ocr.language,
            "translation_confidence": translation.confidence,
        },
    )
