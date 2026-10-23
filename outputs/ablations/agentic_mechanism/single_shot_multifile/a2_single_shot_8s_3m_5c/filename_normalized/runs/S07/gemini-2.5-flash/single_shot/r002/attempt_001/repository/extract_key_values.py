import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_client
from document_models import ExtractedKeyValuePair, KeyValuePair

def extract_key_value_pairs(document_content: bytes) -> ExtractedKeyValuePair:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-document", document_content
    )
    result = poller.result()

    key_value_pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_value_pairs.append(KeyValuePair(
                    key=kv_pair.key.content,
                    value=kv_pair.value.content
                ))

    return ExtractedKeyValuePair(key_value_pairs=key_value_pairs)
