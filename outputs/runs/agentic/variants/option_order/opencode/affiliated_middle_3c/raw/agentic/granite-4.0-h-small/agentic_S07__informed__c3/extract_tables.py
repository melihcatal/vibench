from typing import List, Dict
from .document_models import OCRResponse
from .document_client import create_document_intelligence_client

# Azure Document Intelligence: service=Azure AI Document Intelligence; sdk=azure-ai-documentintelligence; interface=sdk; auth=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY


def extract_tables(ocr_result: OCRResponse) -> List[Dict]:
    # Replace the placeholder with real SDK table parsing logic
    tables = []
    for region in ocr_result.layout:
        if region["type"] == "table":
            tables.append({"rows": region.get("data", [])})
    return tables
