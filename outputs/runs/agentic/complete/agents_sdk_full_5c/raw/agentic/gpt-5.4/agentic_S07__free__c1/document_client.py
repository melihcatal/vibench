from __future__ import annotations

import os
from typing import Iterable, List, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI


DEFAULT_DOCUMENT_MODEL = os.getenv("AZURE_DOCUMENT_MODEL", "prebuilt-layout")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_text_translation_client() -> TextTranslationClient:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    return TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def ensure_bytes(document: bytes | bytearray | memoryview) -> bytes:
    if isinstance(document, bytes):
        return document
    if isinstance(document, bytearray):
        return bytes(document)
    if isinstance(document, memoryview):
        return document.tobytes()
    raise TypeError("document must be bytes-like")


def normalize_sections(sections: Iterable[str]) -> List[str]:
    return [section.strip() for section in sections if section and section.strip()]


def coerce_text(text: Optional[str]) -> str:
    return text.strip() if text else ""
