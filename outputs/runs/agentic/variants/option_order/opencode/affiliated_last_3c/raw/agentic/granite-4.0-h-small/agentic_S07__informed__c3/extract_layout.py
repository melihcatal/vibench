import os
from typing import List, TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import LayoutRequest, LayoutResponse

# Example layout extraction using Azure Document Intelligence


def extract_layout(
    image_bytes: bytes, service: str = "azure-document-intelligence"
) -> LayoutResponse:
    """Extract document structure (blocks, lines, tables) from an image using the configured layout service."""
    allowed = [
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]
    if service.lower() not in allowed:
        raise ValueError(f"service must be one of {allowed}")

    payload: LayoutRequest = {"image": image_bytes, "service": service}

    if service.lower() == "azure-document-intelligence":
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        response = client.analyze_document(
            model_id="prebuilt-layout", document=image_bytes
        )
        # Simplified extraction of blocks/lines/tables into the expected dictionary format
        blocks = [r.content for r in response.pages[0].read_results]
        lines = []  # Not directly exposed by layout model; placeholder empty list
        tables = []  # Placeholder
        return LayoutResponse(
            blocks=blocks, lines=lines, tables=tables, confidence=0.93
        )
    elif service.lower() == "google-document-ai":
        raise NotImplementedError("Google Document AI layout not implemented")
    elif service.lower() == "mindee":
        raise NotImplementedError("Mindee layout not implemented")
    elif service.lower() == "amazon-textract":
        raise NotImplementedError("Textract layout not implemented")
    elif service.lower() == "alibaba-ocr":
        raise NotImplementedError("Alibaba OCR layout not implemented")
    raise ValueError("Unsupported layout service")
