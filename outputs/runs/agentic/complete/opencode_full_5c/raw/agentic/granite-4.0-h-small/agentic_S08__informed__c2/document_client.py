# [HELPER] document_client.py

# Configuration and client utilities for Structured Document Extraction

import os
from typing import Dict, Any

# Supported providers (choose one via env var)
PROVIDERS = {
    "google": {
        "sdk": "google-cloud-documentai",
        "processor_id": "projects/your-project/locations/us-central1/processors/your_invoice_processor",
        "processor_receipt_id": "projects/your-project/locations/us-central1/processors/your_receipt_processor",
        "required_env": ["GOOGLE_APPLICATION_CREDENTIALS"],
    },
    # Add placeholders for other providers if needed
}

# Default provider selected via env var PROVIDER (e.g., PROVIDER=google)
chosen = os.getenv("PROVIDER", "google")
config = PROVIDERS.get(chosen)
if not config:
    raise ValueError(
        f"Unsupported PROVIDER '{chosen}'. Supported: {list(PROVIDERS.keys())}"
    )

# Ensure all env vars are present
missing = [v for v in config["required_env"] if v not in os.environ]
if missing:
    raise RuntimeError(f"Missing env vars for {chosen}: {missing}")

# Create a generic Document AI client factory
from google.cloud import documentai

_client = documentai.DocumentProcessorServiceClient()


_client = documentai.DocumentProcessorServiceClient()


def get_processor_id(document_type: str = "invoice") -> str:
    return (
        config["processor_id"]
        if document_type == "invoice"
        else config["processor_receipt_id"]
    )


def parse_document(file_bytes: bytes, document_type: str = "invoice") -> Dict[str, Any]:
    """Parse a document file using the configured provider and return raw SDK response."""
    # Placeholder: only Google Document AI is implemented
    raw_doc = documentai.Document.from_bytes(file_bytes)
    response = _client.process_document(
        name=get_processor_id(document_type), raw_document=raw_doc
    )
    return response.document
