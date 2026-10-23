import boto3
from document_client import get_textract_client
from document_models import extract_key_value_pairs

def extract_key_values(image_path: str) -> list[tuple[str, str]]:
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    client = get_textract_client()
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    blocks = response['Blocks']
    return extract_key_value_pairs(blocks)