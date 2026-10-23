"""
document_client.py - Local configuration and client helper utilities
for OCR and Layout Extraction tasks.
"""

import os
from typing import Optional, Dict, Any

from document_models import OcrTextResult, LayoutResult, TableResult, KeyValueResult


class DocumentClientConfig:
    """Central configuration for all document processing clients."""

    # Azure Computer Vision (extract_text.py)
    AZURE_CV_ENDPOINT: str = os.environ.get("AZURE_CV_ENDPOINT", "https://YOUR_REGION.api.cognitive.microsoft.com/")
    AZURE_CV_KEY: str = os.environ.get("AZURE_CV_KEY", "")

    # Azure Document Intelligence (extract_layout.py, extract_key_values.py)
    AZURE_DOC_INTELLIGENCE_ENDPOINT: str = os.environ.get("AZURE_DOC_INTELLIGENCE_ENDPOINT", "https://YOUR_REGION.cognitiveservices.azure.com/")
    AZURE_DOC_INTELLIGENCE_KEY: str = os.environ.get("AZURE_DOC_INTELLIGENCE_KEY", "")

    # Google Cloud Document AI (extract_tables.py)
    GOOGLE_CLOUD_PROJECT_ID: str = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    # Azure Translator (ocr_translate.py)
    AZURE_TRANSLATOR_ENDPOINT: str = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com/")
    AZURE_TRANSLATOR_KEY: str = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    AZURE_TRANSLATOR_REGION: str = os.environ.get("AZURE_TRANSLATOR_REGION", "eastus")

    # OpenAI (ocr_safety.py, document_field_extraction.py, ocr_embedding.py)
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

    # Common
    REQUEST_TIMEOUT: int = int(os.environ.get("DOCUMENT_REQUEST_TIMEOUT", "60"))
    MAX_RETRIES: int = int(os.environ.get("DOCUMENT_MAX_RETRIES", "3"))


def get_azure_cv_client():
    """Initialize Azure Computer Vision client for OCR text extraction."""
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    credential = AzureKeyCredential(DocumentClientConfig.AZURE_CV_KEY)
    client = ImageAnalysisClient(
        endpoint=DocumentClientConfig.AZURE_CV_ENDPOINT,
        credential=credential,
    )
    return client


def get_azure_doc_intelligence_client():
    """Initialize Azure Document Intelligence client for layout and key-value extraction."""
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    credential = AzureKeyCredential(DocumentClientConfig.AZURE_DOC_INTELLIGENCE_KEY)
    client = DocumentAnalysisClient(
        endpoint=DocumentClientConfig.AZURE_DOC_INTELLIGENCE_ENDPOINT,
        credential=credential,
    )
    return client


def get_google_documentai_client():
    """Initialize Google Cloud Document AI client for table extraction."""
    from google.cloud import documentai_v1 as documentai

    project_id = DocumentClientConfig.GOOGLE_CLOUD_PROJECT_ID
    location = os.environ.get("GOOGLE_DOC_AI_LOCATION", "us")
    processor_id = os.environ.get("GOOGLE_DOC_AI_PROCESSOR_ID", "document-processor-1")

    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    return client, name


def get_openai_client():
    """Initialize OpenAI client for moderation, field extraction, and embeddings."""
    from openai import OpenAI

    client = OpenAI(
        api_key=DocumentClientConfig.OPENAI_API_KEY,
        base_url=DocumentClientConfig.OPENAI_API_BASE,
    )
    return client


def normalize_image_to_bytes(image_data) -> bytes:
    """Convert various image input formats to raw bytes for API submission."""
    if isinstance(image_data, bytes):
        return image_data
    if hasattr(image_data, "read"):
        return image_data.read()
    if isinstance(image_data, str):
        with open(image_data, "rb") as f:
            return f.read()
    raise TypeError("Unsupported image_data type. Provide bytes, file path, or file object.")


def prepare_text_payload(
    result: OcrTextResult,
    target_language: str = "en",
) -> Dict[str, Any]:
    """Prepare a payload for translation from an OCR result."""
    return {
        "source_text": result.extracted_text,
        "source_language": result.language or "auto",
        "target_language": target_language,
        "confidence": result.confidence,
    }


def prepare_layout_payload(
    result: LayoutResult,
) -> Dict[str, Any]:
    """Prepare a payload for downstream processing from a layout result."""
    blocks = []
    for block in result.blocks:
        blocks.append({
            "content": block.get("content", ""),
            "bounding_box": block.get("bounding_box"),
            "kind": block.get("kind", "unknown"),
        })
    return {
        "blocks": blocks,
        "page_dimensions": result.page_dimensions,
        "model_id": result.model_id,
    }


def prepare_table_payload(
    result: TableResult,
) -> Dict[str, Any]:
    """Prepare a normalized table payload for downstream consumers."""
    tables = []
    for table in result.tables:
        tables.append({
            "row_count": table.get("row_count", 0),
            "column_count": table.get("column_count", 0),
            "cells": table.get("cells", []),
            "bounding_box": table.get("bounding_box"),
        })
    return {
        "tables": tables,
        "page_dimensions": result.page_dimensions,
    }


def prepare_kv_payload(
    result: KeyValueResult,
) -> Dict[str, Any]:
    """Prepare a key-value payload for downstream field extraction."""
    pairs = []
    for kv in result.key_value_pairs:
        pairs.append({
            "key": kv.get("key", ""),
            "value": kv.get("value", ""),
            "confidence": kv.get("confidence", 0.0),
            "bounding_box": kv.get("bounding_box"),
        })
    return {
        "key_value_pairs": pairs,
        "model_id": result.model_id,
    }
