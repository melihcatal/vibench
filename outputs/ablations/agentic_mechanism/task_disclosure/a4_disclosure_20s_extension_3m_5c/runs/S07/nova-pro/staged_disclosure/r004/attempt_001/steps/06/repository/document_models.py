from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import Dict, Any
import boto3

# Initialize the Textract client
textract_client = boto3.client('textract')


def ocr_request(document_bytes: bytes) -> Dict[str, Any]:
    try:
        response = textract_client.detect_document_text(Document={'Bytes': document_bytes})
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise ValueError('Credentials not available') from e


def layout_extraction_request(document_bytes: bytes) -> Dict[str, Any]:
    try:
        response = textract_client.analyze_document(Document={'Bytes': document_bytes}, FeatureTypes=['LAYOUT'])
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise ValueError('Credentials not available') from e


def normalize_ocr_response(response: Dict[str, Any]) -> Dict[str, Any]:
    # Normalization logic for OCR response
    normalized_response = {}
    # Example normalization: extract text
    normalized_response['text'] = ' '.join([item['Text'] for item in response.get('Blocks', []) if item['BlockType'] == 'LINE'])
    return normalized_response


def normalize_layout_response(response: Dict[str, Any]) -> Dict[str, Any]:
    # Normalization logic for Layout Extraction response
    normalized_response = {}
    # Example normalization: extract layout
    normalized_response['layout'] = [item for item in response.get('Blocks', []) if item['BlockType'] == 'LAYOUT_CELL']
    return normalized_response