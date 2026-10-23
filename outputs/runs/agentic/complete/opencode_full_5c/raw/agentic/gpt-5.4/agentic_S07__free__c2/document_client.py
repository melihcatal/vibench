from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI


def get_azure_document_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    resolved_endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    resolved_api_key = api_key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_API_KEY"]
    return DocumentIntelligenceClient(
        endpoint=resolved_endpoint,
        credential=AzureKeyCredential(resolved_api_key),
    )


def get_openai_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> OpenAI:
    resolved_api_key = api_key or os.environ["OPENAI_API_KEY"]
    resolved_base_url = base_url or os.environ.get("OPENAI_BASE_URL")
    kwargs = {"api_key": resolved_api_key}
    if resolved_base_url:
        kwargs["base_url"] = resolved_base_url
    return OpenAI(**kwargs)


def get_default_translation_model() -> str:
    return os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_default_safety_model() -> str:
    return os.environ.get("OPENAI_SAFETY_MODEL", "omni-moderation-latest")


def get_default_extraction_model() -> str:
    return os.environ.get("OPENAI_EXTRACTION_MODEL", "gpt-4.1-mini")


def get_default_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
