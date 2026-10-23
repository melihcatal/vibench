from document_client import DocumentClient
from document_models import extract_layout_elements

def extract_layout(image_path: str) -> list:
    client = DocumentClient()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.analyze_document(image_bytes, ['LAYOUT'])
    blocks = response['Blocks']
    return extract_layout_elements(blocks)
