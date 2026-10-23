from document_client import analyze_document
from document_models import extract_layout

def extract_layout(image_path: str) -> list:
    response = analyze_document(image_path, ['LAYOUT'])
    blocks = response['Blocks']
    return extract_layout(blocks)
