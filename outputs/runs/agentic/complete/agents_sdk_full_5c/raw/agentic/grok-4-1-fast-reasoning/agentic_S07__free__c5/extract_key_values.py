from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_client import AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY

def extract_key_values(image_path: str) -> dict[str, str]:
    """Extracts key-value pairs from a form-like document."""
    client = DocumentAnalysisClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, 
        credential=AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    )
    
    with open(image_path, 'rb') as f:
        data = f.read()
    
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        analyze_request=data,
        content_type="image/jpeg"
    )
    result = poller.result()
    
    kv_map = {}
    for kv_pair in result.key_value_pairs or []:
        if kv_pair.key and kv_pair.value:
            kv_map[kv_pair.key.content.strip()] = kv_pair.value.content.strip()
    return kv_map
