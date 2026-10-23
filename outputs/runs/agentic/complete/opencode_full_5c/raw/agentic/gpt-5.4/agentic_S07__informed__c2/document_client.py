from __future__ import annotations

import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

DEFAULT_AZURE_DI_MODEL = "prebuilt-layout"
DEFAULT_AZURE_DI_INVOICE_MODEL = "prebuilt-invoice"
DEFAULT_AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
DEFAULT_PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = get_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = get_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_document_model_id(default_model: str = DEFAULT_AZURE_DI_MODEL) -> str:
    return os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", default_model)


def get_invoice_model_id() -> str:
    return os.getenv(
        "AZURE_DOCUMENT_INTELLIGENCE_INVOICE_MODEL_ID", DEFAULT_AZURE_DI_INVOICE_MODEL
    )


def get_translator_endpoint() -> str:
    return os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT", DEFAULT_AZURE_TRANSLATOR_ENDPOINT
    ).rstrip("/")


def get_translator_headers() -> dict[str, str]:
    return {
        "Ocp-Apim-Subscription-Key": get_env("AZURE_TRANSLATOR_KEY"),
        "Ocp-Apim-Subscription-Region": get_env("AZURE_TRANSLATOR_REGION"),
        "Content-Type": "application/json",
    }


def get_perspective_endpoint() -> str:
    return DEFAULT_PERSPECTIVE_ENDPOINT


def get_perspective_api_key() -> str:
    return get_env("PERSPECTIVE_API_KEY")


def get_openai_api_key() -> str:
    return get_env("OPENAI_API_KEY")


def get_openai_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBEDDING_MODEL)
