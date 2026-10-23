
from document_client import get_document_intelligence_client
from document_models import DocumentFile, ExtractedKeyValues, ExtractedKeyValuePair

def extract_key_values_from_document(doc: DocumentFile) -> ExtractedKeyValues:
    """
    Extracts key-value pairs from a document image using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()
    
    poller = None
    if doc.file_bytes:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            doc.file_bytes,
            content_type="application/octet-stream"
        )
    elif doc.file_url:
        poller = client.begin_analyze_document(
            "prebuilt-document", {"urlSource": doc.file_url}
        )
    else:
        raise ValueError("DocumentFile must have file_bytes or file_url.")
        
    result = poller.result()

    pairs = []
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key = kvp.key.content if kvp.key else ""
            value = kvp.value.content if kvp.value else None
            if key:
                pairs.append(
                    ExtractedKeyValuePair(
                        key=key,
                        value=value,
                        confidence=kvp.confidence,
                    )
                )

    return ExtractedKeyValues(pairs=pairs, raw_response=result)
