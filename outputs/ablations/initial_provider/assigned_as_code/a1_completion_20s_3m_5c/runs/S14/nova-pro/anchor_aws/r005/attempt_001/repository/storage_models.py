from typing import Dict


def normalize_payload(payload: Dict) -> Dict:
    return {
        'object_name': payload.get('object_name', ''),
        'data': payload.get('data', b''),
        'content_type': payload.get('content_type', 'application/octet-stream')
    }


def parse_response(response: Dict) -> Dict:
    return {
        'object_name': response.get('object_name', '')
    }