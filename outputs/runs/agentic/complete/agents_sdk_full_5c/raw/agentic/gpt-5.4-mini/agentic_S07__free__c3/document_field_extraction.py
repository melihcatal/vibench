from __future__ import annotations

import os

from google.cloud import aiplatform

FIELD_EXTRACTION_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
FIELD_EXTRACTION_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
FIELD_EXTRACTION_MODEL = os.getenv("VERTEX_AI_GEMINI_MODEL", "gemini-1.5-pro-001")


def extract_document_fields(normalized_text: str) -> dict:
    endpoint = f"projects/{FIELD_EXTRACTION_PROJECT}/locations/{FIELD_EXTRACTION_LOCATION}/publishers/google/models/{FIELD_EXTRACTION_MODEL}"
    return {
        "provider": "vertex_ai",
        "model": endpoint,
        "fields": {"document_text": normalized_text},
    }
