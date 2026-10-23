import boto3
from document_client import get_textract_client
from document_models import extract_layout_elements

def extract_layout(image_path: str) -> list[dict]:
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    client = get_textract_client()
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['LAYOUT']
    )
    blocks = response['Blocks']
    return extract_layout_elements(blocks)