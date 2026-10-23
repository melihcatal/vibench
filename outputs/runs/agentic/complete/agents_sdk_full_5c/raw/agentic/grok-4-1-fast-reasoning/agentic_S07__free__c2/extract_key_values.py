from document_client import DocumentClient
from document_models import extract_key_value_pairs

def extract_key_values(image_path: str) -> list:
    client = DocumentClient()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.analyze_document(image_bytes, ['FORMS'])
    blocks = response['Blocks']
    return extract_key_value_pairs(blocks)
