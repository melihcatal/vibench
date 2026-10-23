import os
from typing import BinaryIO
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import KeyValueExtractionResponse, KeyValuePair

def extract_key_values(image_data: BinaryIO) -> KeyValueExtractionResponse:
    """Extract key-value pairs from a form-like document using Azure Form Recognizer."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Form Recognizer credentials not configured.")
    
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document("prebuilt-document", document=image_data.read())
    result = poller.result()
    
    pairs = []
    for kv_pair in result.key_value_pairs:
        pairs.append(KeyValuePair(
            key=kv_pair.key.content if kv_pair.key else "",
            value=kv_pair.value.content if kv_pair.value else "",
            confidence=kv_pair.confidence
        ))
    
    return KeyValueExtractionResponse(
        key_value_pairs=pairs,
        provider="azure_form_recognizer",
        model="prebuilt-document"
    )