
import os
from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValue

def extract_key_values_from_document(document_url: str) -> list[ExtractedKeyValue]:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-document", document_url
    )
    result = poller.result()

    extracted_key_values = []
    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                extracted_key_values.append(
                    ExtractedKeyValue(key=kv_pair.key.content, value=kv_pair.value.content)
                )

    return extracted_key_values
