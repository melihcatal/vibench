from document_client import get_document_client
from document_models import KeyValuePair
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import List

def extract_key_values_from_url(document_url: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document at a URL.
    
    This uses Azure Document Intelligence's prebuilt-document model.
    
    Args:
        document_url: The URL of the document to analyze.
        
    Returns:
        A list of KeyValuePair objects found in the document.
    """
    client = get_document_client()
    
    poller = client.begin_analyze_document_from_url(
        model_id="prebuilt-document",
        url=document_url
    )
    result: AnalyzeResult = poller.result()
    
    extracted_pairs = []
    if result.key_value_pairs:
        for pair in result.key_value_pairs:
            key = pair.key.content if pair.key else ""
            value = pair.value.content if pair.value else ""
            
            if key and value:
                kv_pair = KeyValuePair(
                    key=key,
                    value=value,
                    confidence=pair.confidence
                )
                extracted_pairs.append(kv_pair)
                
    return extracted_pairs
