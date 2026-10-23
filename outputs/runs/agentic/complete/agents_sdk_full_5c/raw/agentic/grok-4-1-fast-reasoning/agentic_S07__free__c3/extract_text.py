from document_client import analyze_document
from document_models import extract_plain_text

def extract_text(image_path: str) -> str:
    response = analyze_document(image_path, ['LAYOUT'])
    blocks = response['Blocks']
    return extract_plain_text(blocks)
