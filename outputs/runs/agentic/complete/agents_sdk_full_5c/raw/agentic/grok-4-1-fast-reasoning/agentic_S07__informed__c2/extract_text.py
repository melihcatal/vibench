import boto3
from document_client import get_textract_client
from document_models import normalize_ocr_text

def extract_text(image_path: str) -> str:
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    client = get_textract_client()
    response = client.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    blocks = response['Blocks']
    return normalize_ocr_text(blocks)