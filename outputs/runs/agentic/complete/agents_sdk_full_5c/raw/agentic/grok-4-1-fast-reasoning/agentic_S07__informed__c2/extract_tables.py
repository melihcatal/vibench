import boto3
from document_client import get_textract_client
from document_models import parse_tables

def extract_tables(image_path: str) -> list[dict]:
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    client = get_textract_client()
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )
    blocks = response['Blocks']
    return parse_tables(blocks)