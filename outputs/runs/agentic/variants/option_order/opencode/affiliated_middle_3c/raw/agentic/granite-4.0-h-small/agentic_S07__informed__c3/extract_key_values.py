from typing import Dict, List
from .document_models import OCRResponse
from .document_client import create_document_intelligence_client

# Azure Document Intelligence: service=Azure AI Document Intelligence; sdk=azure-ai-documentintelligence; interface=sdk; auth=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY


def extract_key_values(ocr_result: OCRResponse) -> List[Dict]:
    # Example placeholder – real implementation would map field names to values
    kv_pairs = []
    for region in ocr_result.layout:
        if region["type"] == "key_value":
            kv_pairs.append(
                {
                    "key": region.get("key_text", ""),
                    "value": region.get("value_text", ""),
                }
            )
    return kv_pairs
