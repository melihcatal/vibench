import io
from document_client import get_document_intelligence_client

def extract_key_values(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-document", # prebuilt-document is good for key-value pairs
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()
    
    key_value_pairs = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                key_value_pairs.append({
                    "key": kv_pair.key.content,
                    "value": kv_pair.value.content
                })

    return {"key_value_pairs": key_value_pairs}
