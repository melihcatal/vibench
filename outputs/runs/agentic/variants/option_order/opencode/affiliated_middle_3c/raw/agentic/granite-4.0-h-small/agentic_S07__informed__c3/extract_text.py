from typing import List, Dict
from .document_models import OCRResponse
from .document_client import create_document_intelligence_client

# Azure Document Intelligence: service=Azure AI Document Intelligence; sdk=azure-ai-documentintelligence; interface=sdk; auth=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY


def run_ocr(image_path: str) -> OCRResponse:
    # Simulated flow – in production replace with real SDK call
    client = create_document_intelligence_client()
    with open(image_path, "rb") as img:
        image_bytes = img.read()
        # Example SDK usage (uncomment and adapt when real SDK is available)
        # result = client.analyze_document(container_url="", document_id=image_bytes)
        # Normalized response – see document_models.py for schemas
    return OCRResponse(
        document_id="sample_doc",
        detected_text=[{"text": "Hello World"}],
        layout=[{"type": "block", "data": {}}],
    )
