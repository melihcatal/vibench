from typing import List, Dict
from .document_models import OCRResponse
from .document_client import create_document_intelligence_client

# Azure Document Intelligence: service=Azure AI Document Intelligence; sdk=azure-ai-documentintelligence; interface=sdk; auth=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY


def extract_layout(ocr_result: OCRResponse) -> List[Dict]:
    # In production: process ocr_result.layout with SDK response parsing
    # Here we return a simple list of named regions (block, line, table) for demo
    layout = []
    for region in ocr_result.layout:
        layout.append({"type": region["type"], "text_preview": region.get("text", "")})
    return layout
