from __future__ import annotations

import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def get_azure_translator_config() -> dict:
    return {
        "endpoint": os.environ.get(
            "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
        ),
        "key": os.environ["AZURE_TRANSLATOR_KEY"],
        "region": os.environ["AZURE_TRANSLATOR_REGION"],
    }


def get_perspective_api_key() -> str:
    return os.environ["PERSPECTIVE_API_KEY"]


def get_document_intelligence_headers() -> dict:
    return {
        "x-ms-client-request-id": "azure-document-intelligence-ocr-layout",
    }
