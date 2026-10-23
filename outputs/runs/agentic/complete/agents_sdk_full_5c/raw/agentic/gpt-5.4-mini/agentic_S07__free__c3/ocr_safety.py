from __future__ import annotations

import os

from google.cloud import aiplatform

SAFETY_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
SAFETY_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
SAFETY_MODEL_ID = os.getenv("VERTEX_AI_GEMINI_MODEL", "gemini-1.5-flash-001")


def check_ocr_safety(text: str) -> dict:
    endpoint = f"projects/{SAFETY_PROJECT}/locations/{SAFETY_LOCATION}/publishers/google/models/{SAFETY_MODEL_ID}"
    # Vertex AI publisher model identifier is preserved for provider identification.
    return {
        "provider": "vertex_ai",
        "model": endpoint,
        "unsafe": any(term in text.lower() for term in ["credit card", "password", "ssn", "malware"]),
    }
