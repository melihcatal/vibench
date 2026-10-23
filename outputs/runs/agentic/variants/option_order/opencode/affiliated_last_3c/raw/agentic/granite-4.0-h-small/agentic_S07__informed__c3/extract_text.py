import os
import typing
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import OCRRequest, OCRResponse

# Example: Azure Document Intelligence OCR (extend for other providers if desired)
# In a real implementation you would call the SDK/client here.


def extract_text(
    image_bytes: bytes, service: str = "azure-document-intelligence"
) -> OCRResponse:
    """Extract plain text from a scanned document image using the configured OCR service."""
    # Validate service choice
    allowed = [
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]
    if service.lower() not in allowed:
        raise ValueError(f"service must be one of {allowed}")

    # Helper to construct request payload
    payload: OCRRequest = {"image": image_bytes, "service": service}

    # Choose runtime logic (SDK vs REST) based on service
    if service.lower() == "azure-document-intelligence":
        # Azure Document Intelligence OCR SDK example
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        # Use the prebuilt OCR model (readLayout) for simplicity
        response = client.analyze_document(
            model_id="prebuilt-read", document=image_bytes
        )
        # Extract text from the SDK response (simplified)
        full_text = "\n".join([r.content for r in response.pages[0].read_results])
        words = [r.content for r in response.pages[0].read_results]
        return OCRResponse(full_text=full_text, words=words, confidence=0.95)

    elif service.lower() == "google-document-ai":
        # Placeholder for Google Document AI SDK usage
        raise NotImplementedError("Google Document AI not implemented in this example")
    elif service.lower() == "mindee":
        # Placeholder for Mindee SDK usage
        raise NotImplementedError("Mindee SDK not implemented in this example")
    elif service.lower() == "amazon-textract":
        # Placeholder for boto3 textract usage
        raise NotImplementedError("Amazon Textract not implemented in this example")
    elif service.lower() == "alibaba-ocr":
        # Placeholder for alibabacloud_ocr_api usage
        raise NotImplementedError("Alibaba OCR not implemented in this example")

    raise ValueError("Unsupported service path")
