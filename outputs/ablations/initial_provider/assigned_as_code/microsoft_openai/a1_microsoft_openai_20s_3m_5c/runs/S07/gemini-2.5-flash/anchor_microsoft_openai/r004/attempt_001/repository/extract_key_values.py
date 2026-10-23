import io
from document_client import get_document_intelligence_client
from document_models import DocumentAnalysisResponse

def extract_key_values(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-document", # Using prebuilt-document model for key-value pairs
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()

    key_value_pairs_data = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_value_pairs_data.append({
                "key": kv_pair.key.content if kv_pair.key else None,
                "value": kv_pair.value.content if kv_pair.value else None,
                "confidence": kv_pair.confidence
            })

    return DocumentAnalysisResponse(key_value_pairs=key_value_pairs_data)._asdict()
