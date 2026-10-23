import os
from typing import TypedDict
from google.api_core.client_options import ClientOptions


class DocumentClientConfig(TypedDict):
    provider: str
    api_key: str
    endpoint: str | None
    project_id: str | None

# Simple registry of provider clients (placeholder for same-scenario OCR)
client_registry = {}

# Example helper: initialize a Google Document AI client
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
def init_google_docai_client() -> DocumentClientConfig:
    config = {
        "provider": "Google Document AI",
        "api_key": GOOGLE_APPLICATION_CREDENTIALS,
        "endpoint": "https://documentai.googleapis.com/v1",
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT")
    }
    client = client_registry.setdefault("google_docai", config)
    return config

# Extend with other providers as needed
