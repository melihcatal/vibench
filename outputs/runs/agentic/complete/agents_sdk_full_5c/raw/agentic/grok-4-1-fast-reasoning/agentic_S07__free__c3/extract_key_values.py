from document_client import analyze_document
from document_models import extract_key_values

def extract_key_values(image_path: str) -> dict:
    response = analyze_document(image_path, ['FORMS'])
    blocks = response['Blocks']
    return extract_key_values(blocks)
