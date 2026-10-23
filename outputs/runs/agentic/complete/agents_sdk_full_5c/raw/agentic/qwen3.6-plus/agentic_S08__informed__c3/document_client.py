"""Provide local configuration and client helper utilities for Structured Document Extraction.

Uses Azure Document Intelligence (azure-ai-documentintelligence) as the concrete provider.
Endpoint: https://<resource>.cognitiveservices.azure.com/
Auth env vars: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

import os
from typing import Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


# Prebuilt model IDs available via Azure Document Intelligence
MODEL_PREBUILT_INVOICE = "prebuilt-invoice"
MODEL_PREBUILT_RECEIPT = "prebuilt-receipt"
MODEL_PREBUILT_LAYOUT = "prebuilt-layout"
MODEL_PREBUILT_READ = "prebuilt-read"


def get_azure_endpoint() -> str:
    """Retrieve Azure Document Intelligence endpoint from environment."""
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        ""
    )
    if not endpoint:
        raise EnvironmentError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT environment variable is not set"
        )
    return endpoint


def get_azure_key() -> str:
    """Retrieve Azure Document Intelligence API key from environment."""
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    if not key:
        raise EnvironmentError(
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variable is not set"
        )
    return key


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """Create and return a configured Azure Document Intelligence client.

    Uses azure-ai-documentintelligence SDK with credentials from environment.
    """
    endpoint = get_azure_endpoint()
    key = get_azure_key()
    credential = AzureKeyCredential(key)
    return DocumentIntelligenceClient(endpoint=endpoint, credential=credential)


def analyze_document(
    file_path: str,
    model_id: str = MODEL_PREBUILT_INVOICE
) -> dict:
    """Analyze a document file using the specified Azure DI model.

    Args:
        file_path: Path to the document file (PDF, image, etc.).
        model_id: Azure Document Intelligence model ID (e.g., 'prebuilt-invoice').

    Returns:
        Parsed document analysis result as a dictionary.
    """
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(model_id=model_id, body=f)
        result = poller.result()

    return _parse_analysis_result(result)


def analyze_document_from_bytes(
    file_bytes: bytes,
    model_id: str = MODEL_PREBUILT_INVOICE,
    content_type: str = "application/pdf"
) -> dict:
    """Analyze document bytes using the specified Azure DI model.

    Args:
        file_bytes: Raw document bytes.
        model_id: Azure Document Intelligence model ID.
        content_type: MIME type of the document.

    Returns:
        Parsed document analysis result as a dictionary.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body=file_bytes,
        content_type=content_type,
    )
    result = poller.result()

    return _parse_analysis_result(result)


def _parse_analysis_result(result) -> dict:
    """Parse Azure Document Intelligence result into a flat dictionary."""
    documents = []
    if result.documents:
        for doc in result.documents:
            doc_data = {
                "doc_type": doc.doc_type,
                "confidence": doc.confidence,
                "fields": {},
            }
            if doc.fields:
                for field_name, field_value in doc.fields.items():
                    doc_data["fields"][field_name] = {
                        "value": field_value.value if hasattr(field_value, "value") else None,
                        "confidence": field_value.confidence if hasattr(field_value, "confidence") else None,
                    }
            documents.append(doc_data)

    return {
        "documents": documents,
        "pages": len(result.pages) if result.pages else 0,
    }
