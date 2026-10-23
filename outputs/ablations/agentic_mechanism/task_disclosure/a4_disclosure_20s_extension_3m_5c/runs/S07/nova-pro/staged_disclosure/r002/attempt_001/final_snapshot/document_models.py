from typing import Dict, Any

import boto3

def create_textract_client():
    return boto3.client('textract')

def create_ocr_request(document_path: str) -> Dict[str, Any]:
    return {
        'Document': {
            'Bytes': open(document_path, 'rb').read()
        }
    }

def create_layout_extraction_request(document_path: str) -> Dict[str, Any]:
    return {
        'Document': {
            'Bytes': open(document_path, 'rb').read()
        },
        'FeatureTypes': ['TABLES', 'FORMS']
    }

def normalize_ocr_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            normalized_response[block['Id']] = block['Text']
    return normalized_response

def normalize_layout_extraction_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            normalized_response[block['Id']] = block
    return normalized_response