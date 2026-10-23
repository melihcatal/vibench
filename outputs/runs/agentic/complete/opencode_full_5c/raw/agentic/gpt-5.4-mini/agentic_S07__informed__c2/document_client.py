import os
from typing import Optional


def get_azure_document_intelligence_endpoint() -> str:
    return os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")


def get_azure_document_intelligence_key() -> str:
    return os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def get_default_model_id() -> str:
    return os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read")


def open_document_bytes(source: str) -> bytes:
    with open(source, "rb") as handle:
        return handle.read()


def get_language(language: Optional[str]) -> Optional[str]:
    return language or os.environ.get("DOCUMENT_LANGUAGE")
