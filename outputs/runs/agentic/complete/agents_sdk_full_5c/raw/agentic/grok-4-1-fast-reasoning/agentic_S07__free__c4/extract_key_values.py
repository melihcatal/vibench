from document_client import get_document_intelligence_client
from document_models import KeyValue
from typing import List
import io

def extract_key_values(image_path: str) -> List[KeyValue]:
    client = get_document_intelligence_client()
    with io.open(image_path, 'rb') as f:
        poller = client.begin_analyze_document("prebuilt-document", analyze_request=f, content_type="application/octet-stream")
    result = poller.result()
    kvs = []
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.key.content and kv_pair.value and kv_pair.value.content:
            kvs.append(KeyValue(
                key=kv_pair.key.content,
                value=kv_pair.value.content,
                confidence=kv_pair.confidence or 0.0
            ))
    return kvs