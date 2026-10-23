from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValue

def extract_key_values_from_document(document_data: bytes) -> list[ExtractedKeyValue]:
    client = get_document_intelligence_client()
    
    # Using prebuilt-document model for general document analysis which includes key-value pairs
    poller = client.begin_analyze_document(model_id="prebuilt-document", document=document_data)
    result = poller.result()
    
    extracted_key_values = []
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            if kvp.key and kvp.value: # Ensure both key and value exist
                key_content = kvp.key.content if kvp.key.content else ""
                value_content = kvp.value.content if kvp.value.content else ""
                extracted_key_values.append(ExtractedKeyValue(
                    key=key_content,
                    value=value_content,
                    page_number=kvp.key.bounding_regions[0].page_number if kvp.key.bounding_regions else None
                ))
                
    return extracted_key_values
