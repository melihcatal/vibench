from typing import List
from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValuePair

def extract_key_values_from_url(url: str) -> List[ExtractedKeyValuePair]:
    """
    Extracts key-value pairs from a document at a given URL.

    Args:
        url: The URL of the document to analyze.

    Returns:
        A list of ExtractedKeyValuePair objects.
    """
    document_intelligence_client = get_document_intelligence_client()

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-document", {"urlSource": url}
    )
    result = poller.result()
    
    kv_pairs = []
    if result.key_value_pairs:
        for pair in result.key_value_pairs:
            key_content = pair.key.content if pair.key else None
            value_content = pair.value.content if pair.value else None
            
            if key_content and value_content:
                 kv_pairs.append(
                    ExtractedKeyValuePair(
                        key=key_content,
                        value=value_content,
                        confidence=pair.confidence,
                    )
                 )
    return kv_pairs
