
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_document_intelligence_client
from document_models import DocumentKeyValue, DocumentExtractionResult
import io

def extract_key_values(payload, config=None):
    config = config or {}
    
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") or config.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    api_key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY") or config.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")

    if not all([endpoint, api_key]):
        raise ValueError("Missing AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or AZURE_DOCUMENT_INTELLIGENCE_API_KEY environment variables/config.")

    client = get_azure_document_intelligence_client(endpoint, api_key)

    poller = client.begin_analyze_document(
        "prebuilt-document", # Use a prebuilt model that supports key-value pairs
        io.BytesIO(payload['document_bytes']),
        content_type=payload['mime_type']
    )
    result = poller.result()

    key_values = []
    for page in result.pages:
        for kv_pair in page.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_values.append(DocumentKeyValue(
                    key=kv_pair.key.content,
                    value=kv_pair.value.content,
                    key_bounding_boxes=[point.x, point.y for point in kv_pair.key.bounding_regions[0].polygon] if kv_pair.key.bounding_regions else [],
                    value_bounding_boxes=[point.x, point.y for point in kv_pair.value.bounding_regions[0].polygon] if kv_pair.value.bounding_regions else []
                ))

    return DocumentExtractionResult(
        text_content=result.content,
        key_values=key_values
    )
