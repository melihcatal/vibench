from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat
from azure.core.credentials import AzureKeyCredential

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://default-doc-intelligence.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api.deepl.com/v2/translate"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

TRANSLATION_MODEL = "gpt-4o"
SAFETY_MODEL = "text-moderation-latest"
FIELD_EXTRACTION_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"


def get_azure_credential() -> AzureKeyCredential:
    if not AZURE_DOCUMENT_INTELLIGENCE_KEY:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variable is required"
        )
    return AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)


def get_document_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    ep = endpoint or AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    cred_key = key or AZURE_DOCUMENT_INTELLIGENCE_KEY
    credential = AzureKeyCredential(cred_key)
    return DocumentIntelligenceClient(endpoint=ep, credential=credential)


def build_azure_poller_kwargs() -> dict:
    return {
        "content_type": "application/json",
        "output_content_format": ContentFormat.MARKDOWN,
    }


def validate_azure_config() -> bool:
    return bool(
        AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY
    )


def validate_deepl_config() -> bool:
    return bool(DEEPL_API_KEY)


def validate_openai_config() -> bool:
    return bool(OPENAI_API_KEY)
