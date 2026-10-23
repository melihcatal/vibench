from document_client import DocumentClient
from document_models import extract_text_from_blocks

def extract_text(image_path: str) -> str:
    client = DocumentClient()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_document_text(image_bytes)
    blocks = response['Blocks']
    return extract_text_from_blocks(blocks)
