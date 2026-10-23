from typing import Dict, Any

def create_request(text: str) -> Dict[str, Any]:
    return {
        'text': text,
    }

def process_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if 'results' in response:
        return response['results']
    return {}

def normalize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in results.items():
        normalized[key] = value.get('normalized', value)
    return normalized
