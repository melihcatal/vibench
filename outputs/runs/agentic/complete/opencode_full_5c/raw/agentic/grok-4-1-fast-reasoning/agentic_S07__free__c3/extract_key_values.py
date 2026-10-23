from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os
from document_client import load_image_bytes
from document_models import KeyValuesResult


def extract_key_values(image_path: str) -> KeyValuesResult:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    content = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-document", document=content, content_type="image/jpeg"
    )
    result = poller.result()
    pairs = []
    for document in result.documents:
        for kv_pair in getattr(document, "key_value_pairs", []):
            if kv_pair.key and kv_pair.value:
                pairs.append(
                    {
                        "key": kv_pair.key.content,
                        "value": kv_pair.value.content,
                        "confidence": getattr(kv_pair, "confidence", 0.0),
                    }
                )
    return {"pairs": pairs}
