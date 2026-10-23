from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': payload.get('text', '')}


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {'toxicity': max((category.get('severity', 0) for category in response.get('categories_analysis', [])), default=0) / 7}