from typing import Any, Dict, List

import boto3

def create_textract_client() -> boto3.client:
    return boto3.client('textract')

def create_ocr_request(document_bytes: bytes) -> Dict[str, Any]:
    return {
        'Document': {
            'Bytes': document_bytes
        }
    }

def create_layout_request(document_bytes: bytes) -> Dict[str, Any]:
    return {
        'Document': {
            'Bytes': document_bytes
        }
    }

def normalize_ocr_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_response = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            normalized_response.append({
                'text': item.get('Text', ''),
                'confidence': item.get('Confidence', 0.0)
            })
    return normalized_response

def normalize_layout_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_response = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LAYOUT_CELL':
            normalized_response.append({
                'text': item.get('Text', ''),
                'confidence': item.get('Confidence', 0.0)
            })
    return normalized_response