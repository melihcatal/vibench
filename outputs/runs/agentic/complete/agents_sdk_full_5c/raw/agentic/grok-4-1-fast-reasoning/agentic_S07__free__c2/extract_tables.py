from document_client import DocumentClient
from document_models import extract_tables

def extract_tables(image_path: str) -> list:
    client = DocumentClient()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.analyze_document(image_bytes, ['TABLES'])
    blocks = response['Blocks']
    return extract_tables(blocks)
