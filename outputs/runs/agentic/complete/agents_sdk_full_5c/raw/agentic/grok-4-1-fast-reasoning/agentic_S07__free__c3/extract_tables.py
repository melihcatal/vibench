from document_client import analyze_document
from document_models import extract_tables

def extract_tables(image_path: str) -> list:
    response = analyze_document(image_path, ['TABLES'])
    blocks = response['Blocks']
    return extract_tables(blocks)
