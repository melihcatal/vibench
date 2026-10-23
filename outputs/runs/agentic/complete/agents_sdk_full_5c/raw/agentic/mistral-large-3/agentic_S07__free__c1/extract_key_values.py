import os
from typing import BinaryIO, Dict
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import KeyValueResponse

def extract_key_values(image_data: BinaryIO) -> Dict[str, KeyValueResponse]:
    """Extract key-value pairs from a form-like document using Azure Form Recognizer."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Form Recognizer credentials not configured.")
    
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document("prebuilt-document", document=image_data.read())
    result = poller.result()
    
    key_values = {}
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            key_values[kv_pair.key.content] = KeyValueResponse(
                key=kv_pair.key.content,
                value=kv_pair.value.content,
                confidence=kv_pair.confidence
            )
    
    return key_values