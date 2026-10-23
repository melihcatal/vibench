from typing import Any, Dict, List

def create_safety_request(text: str) -> Dict[str, Any]:
    return {
        'text': text,
    }

def parse_safety_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if 'results' in response:
        return response['results']
    return {}

def normalize_safety_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_results = []
    for result in results:
        normalized_result = {
            'category': result.get('category', ''),
            'severity': result.get('severity', ''),
            'probability': result.get('probability', 0.0),
        }
        normalized_results.append(normalized_result)
    return normalized_results