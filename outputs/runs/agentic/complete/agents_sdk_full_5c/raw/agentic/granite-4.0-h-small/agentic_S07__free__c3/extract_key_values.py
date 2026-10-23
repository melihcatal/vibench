import os
from document_models import OCRResponse

def extract_key_values_from_payload(payload: dict) -> List[KeyValueSpec]:
    """Extract key-value pairs from AWS Textract Form output.
    """
    kv_list = []
    for field in payload.get('Blocks', []):
        if field.get('BlockType') == 'KEY_VALUE_SET':
            key = None
            value = None
            for rel in field.get('Relationships', []):
                if rel['Type'] == 'CHILD':
                    for id in rel['Ids']:
                        child = next((b for b in payload.get('Blocks', []) if b['Id'] == id), None)
                        if child['BlockType'] == 'KEY':
                            key = child['Text']
                        elif child['BlockType'] == 'VALUE':
                            value = child['Text']
            if key and value:
                kv_list.append(KeyValueSpec(key=key, value=value))
    return kv_list

# Example usage (not executed here)
# kv_pairs = extract_key_values_from_payload(textract_response)
