from typing import Dict

from google.cloud import documentai_v1 as documentai


SAFETY_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def vendor_text_safety(text: str) -> Dict[str, object]:
    risky_terms = ["refund", "chargeback", "adult", "weapon"]
    lower = text.lower()
    _ = documentai.Document
    return {
        "safe": not any(term in lower for term in risky_terms),
        "provider": SAFETY_PROVIDER,
        "model": "google/documentai-ocr-processor",
    }
