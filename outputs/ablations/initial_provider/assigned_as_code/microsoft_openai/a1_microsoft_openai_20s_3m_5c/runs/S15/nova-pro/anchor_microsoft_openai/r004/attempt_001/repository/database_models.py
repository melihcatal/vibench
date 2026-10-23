from typing import Dict


def normalize_document(document: Dict) -> Dict:
    return {k: v for k, v in document.items() if k!= 'id'}


def parse_response(response: Dict) -> Dict:
    return {k: v for k, v in response.items() if k!= '_etag'}