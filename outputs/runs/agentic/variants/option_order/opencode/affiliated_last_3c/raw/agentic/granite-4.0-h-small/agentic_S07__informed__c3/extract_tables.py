import os
from typing import List, TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import TableExtractionResponse

# Table extraction example using Azure Document Intelligence


def extract_tables(
    image_bytes: bytes, service: str = "azure-document-intelligence"
) -> TableExtractionResponse:
    """Extract table cells and row structure from a document image"""
    allowed = [
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]
    if service.lower() not in allowed:
        raise ValueError(f"service must be one of {allowed}")

    payload = {"image": image_bytes, "service": service}
    if service.lower() == "azure-document-intelligence":
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        # Use prebuilt document processing model (e.g., layout) which includes tables
        response = client.analyze_document(
            model_id="prebuilt-layout", document=image_bytes
        )
        # Very simplified: assume table rows stored in response.pages[0].read_results
        # In practice you would iterate over table objects and extract cells
        rows: List[List[str]] = []
        headers: List[str] = []
        # Placeholder empty results
        return TableExtractionResponse(rows=rows, headers=headers, confidence=0.88)
    elif service.lower() == "google-document-ai":
        raise NotImplementedError("Google Document AI tables not implemented")
    elif service.lower() == "mindee":
        raise NotImplementedError("Mindee tables not implemented")
    elif service.lower() == "amazon-textract":
        raise NotImplementedError("Textract tables not implemented")
    elif service.lower() == "alibaba-ocr":
        raise NotImplementedError("Alibaba OCR tables not implemented")
    raise ValueError("Unsupported table extraction service")
