from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValuePair, ExtractedText

def extract_key_values_from_document(document_data: bytes, content_type: str) -> list[ExtractedKeyValuePair]:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(model_id="prebuilt-document", document=document_data, content_type=content_type)
    result = poller.result()

    extracted_key_values = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key_text = ExtractedText(text=kv_pair.key.content if kv_pair.key else "")
            value_text = ExtractedText(text=kv_pair.value.content if kv_pair.value else "")
            extracted_key_values.append(ExtractedKeyValuePair(key=key_text, value=value_text, confidence=kv_pair.confidence))
    
    return extracted_key_values
